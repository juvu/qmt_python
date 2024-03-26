# encoding:gbk
'''
本策略事先设定好交易的股票篮子，然后根据指数的CCI指标来判断超买和超卖
当有超买和超卖发生时，交易事先设定好的股票篮子
'''
import pandas as pd
import numpy as np
import talib
import time

######################PD 格式设置###########################
pd.set_option('expand_frame_repr', False)  # 不换行
pd.set_option('display.max_rows', 5000)  # 最多显示数据的行数
pd.set_option('display.unicode.ambiguous_as_wide', True)  # 中文字段对齐
pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.float_format', lambda x: '%.2f' % x)


##########################################################


# ####################参数配置说明###########################
# real   1:实盘    	0：模拟帐号
# log    1:打印日记   	0：不打印日记
# scale  仓位控制   开仓数据为  1/scale  数值越大，开仓越小
# buy_num   买入一支股票，是否分几次买入
###########################################################

class Tool():
    def __init__(self, ContextInfo):
        self.g = ContextInfo
        print('自定义工具类')

    def log(self, *args):
        # log 为用户输入参数
        if log:
            print(*args)

    def readStockInfo(self, st):
        # 读取个股的基本信息
        start_time = self.g.get_open_date(st)
        # detail CreateDate:上市日期 ,FloatVolumn：流通股本,TotalVolumn：总股本
        detail = self.g.get_instrumentdetail(st)
        data = {}
        data['code'] = st
        data['start_time'] = str(detail['CreateDate'])
        data['FloatVolumn'] = np.int64(detail['FloatVolumn'])
        data['TotalVolumn'] = np.int64(detail['TotalVolumn'])
        series = pd.Series(data)
        self.g.stockinfo[st] = series

    # return series
    def readMyStock(self, bkname):
        # 读取自选股列表
        self.g.trade_code_list = self.g.get_stock_list_in_sector(bkname)
        self.g.set_universe(self.g.trade_code_list)
        self.g.stock_count = len(self.g.trade_code_list)

    def readStockData(self, columns=['close', 'open', 'high', 'low', 'volume', 'settle'], per='1d', size=10):
        # 读取股票行情数据
        self.g.df = self.g.get_market_data(columns, stock_code=self.g.trade_code_list, skip_paused=True, period=per, dividend_type='front', count=size)

    def readStockDataTick(self):
        # 读取列表中的股票的盘口数据
        self.g.df_tick = self.g.get_full_tick(self.g.trade_code_list)
        self.log(type(self.g.df_tick))

    def doRead(self, bkname):
        self.readMyStock(bkname)
        if self.g.stock_count == 0:
            print('当前板块没有数据，请添加股票到板块列表中！')
            self.g.df_type = 0
            return
        # 读取股票的盘口数据
        self.readStockDataTick()
        # 读取股票的行情数据
        self.readStockData()
        self.log('行情数据:', type(self.g.df))
        if isinstance(self.g.df, pd.DataFrame):
            self.log('DF 数据格式为DataFrame')
            self.g.df_type = 1
            return
        elif isinstance(self.g.df, pd.Panel):
            self.log('DF 数据格式为Panel')
            self.g.df_type = 2
            return
        else:
            self.g.df_type = 0
            return

    def formatDf(self, st, df):
        # 个股数据的格式化
        df_infos = self.g.stockinfo
        if st not in df_infos.columns:
            self.readStockInfo(st)
        if st not in df_infos.columns:
            return
        stock_info = self.g.stockinfo[st]
        self.log('info:', stock_info)

        # 计算涨跌停价
        bd = 0.1
        code = int(st.split('.')[0])
        nc = code // 100000
        if nc == 3:
            bd = 0.2
        elif nc == 6:
            nc = code // 10000
            if nc == 68:
                bd = 0.2
        # bd值为股票的涨跌幅限制  创业板、科创板为0.2  其余的为0.1

        # 格式化数据
        df['old_close'] = df['close'].shift(1)
        # 求出今天的			开盘价震幅
        df['open_offset'] = (df['open'] - df['old_close']) * 100 / df['old_close']
        # 求出当前收盘价			是否接近涨停
        df['now_offset'] = (df['close'] - df['old_close']) * 100 / df['old_close']
        # 算出每天的			涨停价
        df['top'] = df['old_close'] * (1 + bd)
        df['top'] = df['top'].apply(lambda x: round(x, 2))
        # 算出每天的			跌停价
        df['fail'] = df['old_close'] * (1 - bd)
        df['fail'] = df['fail'].apply(lambda x: round(x, 2))
        # 盘中				是否上摸涨停价
        df['istop'] = df['top'] == df['high']
        # 盘中				是否触及跌停价
        df['isfail'] = df['low'] == df['fail']
        # 当前收盘是否			涨停
        df['istopnow'] = df['top'] == df['close']
        # 当前收盘价是			跌停
        df['isfailnow'] = df['low'] == df['close']
        # 当前				K线换手率
        df['hand'] = df['volume'] / stock_info['FloatVolumn'] * 10000
        # 当前K线				是否红盘  -		股价一直在开盘价上方运行
        df['isred'] = df['low'] >= df['open']
        # 当前K线				是否为阳线
        df['issun'] = df['close'] >= df['open']
        return df

    def modelDb(self, st, df):
        # 判断当前股票是否符合打板条件 模型算法 符合条件返回 True 否则 False
        # 取出该股票的盘口数据
        # self.log(st,df)
        ndata = df.iloc[-1]
        self.log('当日实时数据', ndata)
        ndata = pd.Series(ndata)
        ndata['buy'] = False

        tick = self.g.df_tick[st]
        sellPrice = tick['askPrice']
        count = 0
        for i in range(0, 5):
            if sellPrice[i] == ndata['top']:
                count = i + 1
                break
        self.log('count=', count)
        if count == 0:
            return ndata
        if count <= offset and ndata['istop']:
            ndata['buy'] = True
            ndata['buy_price'] = sellPrice[count]
        return ndata


def init(ContextInfo):
    # hs300成分股中sh和sz市场各自流通市值最大的前3只股票
    ContextInfo.trade_code_list = []
    ContextInfo.set_universe(ContextInfo.trade_code_list)
    ContextInfo.stock_count = 0

    ContextInfo.accID = '410038217334'
    ContextInfo.buy = True
    ContextInfo.sell = False
    # 股票的实时行情数据
    ContextInfo.df = None
    ContextInfo.df_type = 0
    # 股票的实时盘口数据
    ContextInfo.df_tick = None
    # ContextInfo.colums=['close','open','high','low','volume','settle']
    ContextInfo.tick = 0
    # 股票列表中个股的基本信息
    ContextInfo.stockinfo = pd.DataFrame()
    # 自定义工具类
    ContextInfo.tool = Tool(ContextInfo)


# 设置定时器，执行自定义运行  5nSecond,,500nMilliSecond
# ContextInfo.run_time("myHandlebar","5nSecond","2019-10-14 13:20:00","SH")


def myHandlebar(g):
    # tool = g.tool
    # tool.doRead('我的自选')
    return


# 自定义的交易函数
# ContextInfo.tick = ContextInfo.tick + 1
# print(ContextInfo.tick)
# readData(ContextInfo)

def handlebar(g):
    tool = g.tool
    # g.tool.formatFloat(1)
    if g.is_last_bar():
        # 为行情数据的格式，df_type   0:不处理  1：DataFrame  2:Panel
        df = None
        tool.doRead('我的自选')
        if g.df_type == 0:
            return
        if g.df_type == 1:
            df = g.df
            st = g.trade_code_list[0]
            df = tool.formatDf(st, df)
            ndata = tool.modelDb(st, df)
            isbuy(g, st, ndata)
        elif g.df_type == 2:
            for st in g.trade_code_list:
                df = g.df[st]
                df = tool.formatDf(st, df)
                ndata = tool.modelDb(st, df)
                isbuy(g, st, ndata)


def isbuy(g, st, ndata):
    # 是否执行股票买入操作
    print(ndata)
    if ndata['buy']:
        print('股票开仓：', st, ndata)
    pass



















