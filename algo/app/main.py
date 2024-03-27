from datetime import datetime, timedelta, time
import json
import os
import queue
import socket
import threading
import time as t
import webbrowser
import pywencai as wc
import pandas as pd
import redis
import qstock as qs


import uvicorn
from fastapi import FastAPI


import logging

from routers import items

logging.basicConfig(
    level=logging.NOTSET,
    filename='./algo/app/default.log'
)


app = FastAPI()
app.include_router(items.router)
public_obj = {'code_list': [],
              }

def print_(str_obj, directory="algo/app/logs"):
    print(str_obj)
    logging.log(logging.INFO,str_obj)
    # 确保提供的目录存在
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
        # 获取当前时间
    current_time = t.localtime()
    
    # 根据当前时间生成文件名
    file_name = t.strftime("data_log_%Y-%m-%d-%H-%M.txt", current_time)
    
    # 将分钟数转换为离最近的10分钟整数倍的时间（向下取整）
    minute = current_time.tm_min - (current_time.tm_min % 10)
    file_name = t.strftime(f"data_log_%Y-%m-%d-%H-{minute:02d}.txt", current_time)
    
    if directory:
        file_path = os.path.join(directory, file_name)
    else:
        file_path = file_name
    
    # 写入数据到文件
    with open(file_path, 'a') as file:
        file.write(str(str_obj) + "\n")

    # 上面的代码会在example.txt文件末尾追加内容 "Goodbye, World!"

    
    

def brain_init():
    character = "radicalise"  # 激进性格


def brain_bidding():
    """
    竞价:分析竞价
    """
    pass


def get_trade_date(day: int = 0):
    """
    获取交易日
    """
    days_to_subtract = 5
    skipped_days = 0

    while skipped_days < days_to_subtract:
        current_date = datetime.now()
        current_date = current_date - timedelta(days=day)
        if current_date.weekday() < 5:  # 周一到周五为0-4
            skipped_days += 1
        else:
            day += 1
    return current_date.strftime('%Y%m%d')

def brain_zgl():
    """
    诸葛亮、荀彧:分析市场
    """
    pass

def wencai_():

    def brain_think(res, ideal):
        """
        分析数据
        """
        print_(ideal)

        # 回忆：都数据库中取出数据,然后分析
        # 读redis或者es然后分析
        code_list = []
        def get_code_info(stock_info):
            if '股票代码' in stock_info.keys(): stock_info['股票代码']                                                                          #   001282.SZ
            if '股票简称' in stock_info.keys(): stock_info['股票简称']                                                                          #   三联锻造
            if '最新价' in stock_info.keys(): stock_info['最新价']                                                                            #   32.20
            if '最新涨跌幅' in stock_info.keys(): stock_info['最新涨跌幅']                                                                            #   0.846
            master_money_str = '主力资金流向'                                                                            #   
            current_date = get_trade_date(0)                                                                            #   
            # 市值
            if f'a股市值(不含限售股)[{current_date}]' in stock_info.keys():
                market_value = int(float(stock_info[f'a股市值(不含限售股)[{current_date}]']))/10000                                                     # 9.144036
            # 资金买卖
            # 资金净流入
            if f'资金流入inner[{current_date}]' in stock_info.keys() and f'主力买入金额[{current_date}]' in stock_info.keys():
                net_capital_inflow = (float(stock_info[f'资金流入inner[{current_date}]']) - float(stock_info[f'资金流出inner[{current_date}]'])) / 10000
                main_net_buying = (float(stock_info[f'主力买入金额[{current_date}]']) - float(stock_info[f'主力卖出金额[{current_date}]']))/ 10000
                net_capital_inflow / market_value
                main_net_buying / market_value
            if f'dde散户数量[{current_date}]' in stock_info.keys():
                stock_info[f'dde散户数量[{current_date}]']
            res = wc.get(query=f'{stock_info["股票简称"]}散户情况', )
            if 'barline3' in res.keys(): 
                print_(res['barline3'])
                if 'dde散户数量' in res['barline3'].keys(): print_(res['barline3']['dde散户数量'].astype(float).sum())
            if '多日累计dde散户数量' in res.keys(): print_(res['多日累计dde散户数量'])
            if '文本标题h1' in res.keys(): print_(res['文本标题h1'])
            # if 'txt1' in res.keys():
                # print_(res['txt1'])
            
         # print_(pd.merge(res['barline3'], res['历史主力资金流向']['barline3']))
            code_list.append(stock_info['code'])

        if 'apply' in dir(res): res.apply(get_code_info, axis=1)
        print_(code_list)
        # res_list = res.to_dict(orient='records')
        # res_code_list = [i['股票代码'] for i in res_list]
        # for i in res_code_list:
        #     code_info = wc.get(query=i)
        # public_obj['code_list'] = res.to_dict(orient='records')
    def brain_think_ascending_channel(res, ideal):
        """
        上升通道
        散户会有很多散户持有一个股票,出现一个股票多个散户持有是正常的情况
        """
        print_('上升通道')
        print_(ideal)

        def get_code_info(stock_info):
            stock_info['股票代码']
            stock_info['股票简称']
            stock_info['最新价']
            stock_info['最新涨跌幅']

        res.apply(get_code_info, axis=1)
        res_list = res.to_dict(orient='records')
        res_code_list = [i['股票代码'] for i in res_list]
        # for i in res_code_list:
        #     code_info = wc.get(query=i)
        public_obj['code_list'] = res.to_dict(orient='records')
        print_(res)
    def brain_think_private_investor(res, ideal):
        """
        分析散户
        散户会有很多散户持有一个股票,出现一个股票多个散户持有是正常的情况
        """
        print_('分析散户')
        print_(ideal)
        res_list = res.to_dict(orient='records')
        res_code_list = [i['股票代码'] for i in res_list]
        # for i in res_code_list:
        #     code_info = wc.get(query=i)
        public_obj['code_list'] = res.to_dict(orient='records')
        print_(res)
    current_time = datetime.now().time()
    start_time = time(9, 10)
    end_time = time(9, 30)

    while True:
        if start_time <= current_time <= end_time:
            ideals = ['9:20之前的竞价出现涨跌停价挂单加分,剔除ST',
                      '9:20~9:25期间,撮合价格逐步走高,同时伴随着成交量的放大,且以密集红柱为主。最好在最后一两分钟内 有快速拉高(大资金强吃货),且最终竞价涨幅在3%~7%之间',
                      '9:30前,有巨单挂过涨跌停价,个股形态完好,前几日分时有过异动或者有过涨停,开始股价涨停 ,竞价过程中撮合价格慢慢走低,但成交量有效放大,并且承接很好,主买盘为主', ]
            sleep_time = 60
        else:
            ideals = ['市值小于50亿,剔除ST,缩量,最近10个交易日有6个交易日以上主力资金净流入,最近3个交易日涨幅为正,资金净流入的股票,散户卖出,筹码高度集中,MACD大于0,',
                      '市值小于50亿,散户持续卖出,放量,剔除ST,剔除次新,亿剔除次北交所,最近10个交易日有6个交易日以上主力资金净流入,最近3个交易日涨幅为正,',
                      '市值小于50亿,放量,不包括次新股,剔除ST,剔除次新,亿剔除次北交所,股票市场不包括北交所,散户卖出,',
                      '机构净额大于500万,关注度高,近期热门板块,散户卖出,',
                      '市值小于50亿,放量,剔除ST,剔除次新,剔除北交所,拉升通道,最近20日放量,',
                      '市值小于100亿,亿剔除次新股,拉升通道,股票市场只包括创业板,MACD大于0,资金流入,最近20日放量,',
                      '市值小于100亿,拉升,仅创业板,剔除ST,散户持续卖出,MACD大于0,业绩预增大于20%,筹码高度集中,资金流入,最近20日放量,',
                      # AI模型精选优质股
                      '小盘股(流通市值小于100亿),日线放量上涨,macd提示买入',
                      '业绩预增大于20%,机构评级看多',
                      '龙虎榜净买入,昨日放量上涨,短期趋势向上',
                      ]
            sleep_time = 600
        current_time = datetime.now().time()
        time1 = time(9, 10)
        time2 = time(11, 30)
        time3 = time(13, 0)
        time4 = time(15, 20)
        if time1 <= current_time <= time2 or time3 <= current_time <= time4:            # 程序9.10分-11.30分,13.00-15.00运行时间
        # if True:            # 程序9.10分-11.30分,13.00-15.00运行时间
            for ideal in ideals:
                print_(ideal)
                try:
                    res = wc.get(query=ideal)
                except Exception as e:
                    webbrowser.open('https://www.iwencai.com/unifiedwap/reptile.html?returnUrl=https%3A%2F%2Fwww.iwencai.com%2Funifiedwap%2Fhome%2Findex%3Fsign%3D1709793871013&sessionId=117.30.119.18&antType=unifiedwap')
                    print_(e)
                    t.sleep(15)
                    continue
                print_(res)
                if res is not None:
                    if '散户持续买入' in ideal:
                        brain_think_private_investor(res, ideal)
                    elif '拉升通道' in ideal:
                        brain_think_ascending_channel(res, ideal)
                    else:
                        brain_think(res, ideal)
        t.sleep(sleep_time)
        # public_obj['code_list'] = res.rename(columns={'股票代码': 'code', '股票简称': 'name', '最新价': 'price'}).loc[:, ['code', 'name', 'price']].drop_duplicates().to_dict(orient='records')


def brain_buy():
    pass


def brain_sell():
    pass


def brain_analyse_BX():
    """
    分析北向资金
    """
    pass


def brain_analyse_CY():
    """
    分析创业板stock
    """
    pass


def brain_analyse_SH():
    """
    分析上证指数,
    根据历史走势,近期热点板块,列入观察列表
    """
    pass


def watch_list():
    """
    观察列表,是否观察到了大额度的交易,涨停前的具体表现就是大单子上推
    """
    pass


# 创建一个 Redis 客户端对象
# client = redis.Redis(host='localhost', port=6379, db=1, password='123456')
# namespace_prefix = 'data:'
# 获取一个键值对
# value = client.get(namespace_prefix+'拉升通道')
# print_(value)
# 关闭 Redis 客户端对象
# https://www.iwencai.com/unifiedwap/result?w=%E5%89%94%E9%99%A4%E6%AC%A1%E6%96%B0%E8%82%A1%EF%BC%9B%E5%89%94%E9%99%A4st%E8%82%A1%EF%BC%9B%E6%8B%89%E5%8D%87%E9%80%9A%E9%81%93%EF%BC%8C&querytype=stock
# https://backtest.10jqka.com.cn/
# print_('记住dde散户数量最重要~~~~~')


# ['__class__', '__deepcopy__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'barpos', 'benchmark', 'bsm_iv', 'bsm_price', 'capital', 'context', 'create_sector', 'current_bar', 'data_info_level', 'dividend_type', 'do_back_test', 'draw_icon', 'draw_number', 'draw_text', 'draw_vertline', 'end', 'get_ETF_list', 'get_all_subscription', 'get_back_test_index', 'get_bar_timetag', 'get_bvol', 'get_close_price', 'get_commission', 'get_contract_expire_date', 'get_contract_multiplier', 'get_date_location', 'get_divid_factors', 'get_factor_data', 'get_finance', 'get_financial_data', 'get_float_caps', 'get_full_tick', 'get_function_line', 'get_his_contract_list', 'get_his_index_data', 'get_his_st_data', 'get_history_data', 'get_hkt_details', 'get_hkt_statistics', 'get_holder_num', 'get_industry', 'get_instrumentdetail', 'get_largecap', 'get_last_close', 'get_last_volume', 'get_local_data', 'get_longhubang', 'get_main_contract', 'get_market_data', 'get_market_data_ex', 'get_market_data_ex_ori', 'get_midcap', 'get_net_value', 'get_north_finance_change', 'get_open_date', 'get_option_detail_data', 'get_option_iv', 'get_option_list', 'get_option_undl', 'get_option_undl_data', 'get_product_asset_value', 'get_product_init_share', 'get_product_share', 'get_raw_financial_data', 'get_risk_free_rate', 'get_scale_and_rank', 'get_scale_and_stock', 'get_sector', 'get_slippage', 'get_smallcap', 'get_stock_list_in_sector', 'get_stock_name', 'get_stock_type', 'get_svol', 'get_tick_timetag', 'get_top10_share_holder', 'get_total_share', 'get_tradedatafromerds', 'get_trading_dates', 'get_turn_over_rate', 'get_turnover_rate', 'get_universe', 'get_weight_in_index', 'in_pythonworker', 'is_fund', 'is_future', 'is_last_bar', 'is_new_bar', 'is_stock', 'is_suspended_stock', 'load_stk_list', 'load_stk_vol_list', 'market', 'paint', 'period', 'refresh_rate', 'request_id', 'run_time', 'set_account', 'set_commission', 'set_slippage', 'set_universe', 'start', 'stockcode', 'stockcode_in_rzrk', 'subMap', 'subscribe_quote', 'subscribe_whole_quote', 'time_tick_size', 'unsubscribe_quote', 'z8sglma_last_barpos', 'z8sglma_last_version']
# ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__instance_size__', '__le__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'm_Enable', 'm_dAssetBalance', 'm_dAssureAsset', 'm_dAvailable', 'm_dBalance', 'm_dBuyWaitMoney', 'm_dCashIn', 'm_dCloseProfit', 'm_dCommission', 'm_dCredit', 'm_dCurrMargin', 'm_dDeposit', 'm_dEntrustAsset', 'm_dFetchBalance', 'm_dFrozenCash', 'm_dFrozenCommission', 'm_dFrozenMargin', 'm_dFrozenRoyalty', 'm_dFundValue', 'm_dGoldFrozen', 'm_dGoldValue', 'm_dInitBalance', 'm_dInitCloseMoney', 'm_dInstrumentValue', 'm_dInstrumentValueRMB', 'm_dIntradayBalance', 'm_dIntradayFreedBalance', 'm_dLoanValue', 'm_dLongValue', 'm_dMargin', 'm_dMaxMarginRate', 'm_dMortgage', 'm_dNav', 'm_dNetValue', 'm_dOccupiedBalance', 'm_dPositionProfit', 'm_dPreBalance', 'm_dPreCredit', 'm_dPreMortgage', 'm_dPurchasingPower', 'm_dRawMargin', 'm_dRealRiskDegree', 'm_dRealUsedMargin', 'm_dReceiveInterestTotal', 'm_dRepurchaseValue', 'm_dRisk', 'm_dRoyalty', 'm_dSellWaitMoney', 'm_dShortValue', 'm_dStockValue', 'm_dSubscribeFee', 'm_dTotalDebit', 'm_dWithdraw', 'm_nBrokerType', 'm_nDirection', 'm_strAccountID', 'm_strAccountKey', 'm_strAccountRemark', 'm_strBrokerName', 'm_strMoneyType', 'm_strOpenDate', 'm_strStatus', 'm_strTradingDate']
def print_data(data):
    if data is None: return
    data = data['xuangu_tableV1']
    data.rename(columns={'股票简称': 'name', '最新价': 'price'}, inplace=True)
    data.sort_values(by='code', ascending=True, inplace=True, )
    data = data.loc[:, ['code', 'name', 'price']].drop_duplicates()
    for row in data.iterrows():
        try:
            result_set = wc.get(query=row[1]['name'], )
            df3 = pd.merge(result_set['barline3'], result_set['历史主力资金流向']['barline3'])
            result_set['barline3']
            result_set['所属概念列表']
            result_set['历史主力资金流向']['barline3']
            result_set['kline2']
            result_set['估值指标']['市盈率']['labelLine']
            result_set['估值指标']['市净率']['labelLine']
            result_set['估值指标']['市销率']['labelLine']
            print_(df3)
        except Exception as e:
            print_(e)


def analyse():
    # now = datetime.datetime.now()
    # day = now.strftime("%Y-%m-%d")
    # if not os.path.exists(f"{day}"):
    #     os.mkdir(f"{day}")
    # # namespace_prefix = 'data:'
    # # namespace_prefix = namespace_prefix + day
    # res = wc.get(query='市值小于50亿；即将启动拉升；剔除次新股；剔除st股股票市场不包括北交所,剔除创业板股票')
    # print_('------------------------即将启动拉升----------------------------')
    # print_(res['xuangu_tableV1'])
    # if res is not None: client.set(namespace_prefix + '即将启动拉升', json.dumps(list(set([i for i in res['xuangu_tableV1']['股票代码']]))))
    # print_(res['xuangu_tableV1'])
    # print_data(res)
    # res = wc.get(query='市值小于50亿；上升趋势；剔除次新股；剔除st股；股票市场不包括北交所,剔除创业板股票')
    # print_('------------------------市值小于60亿上升趋势----------------------------')
    # if res is not None: client.set(namespace_prefix + '上升趋势', json.dumps(list(set([i for i in res['xuangu_tableV1']['股票代码']]))))
    # print_(res['xuangu_tableV1'])
    # print_data(res)
    # res = wc.get(query='市值小于100亿,亿剔除次新股；剔除st股；拉升通道,股票市场不包括北交所,剔除创业板股票')
    # print_('------------------------市值小于100亿,拉升通道----------------------------')
    # if res is not None: client.set(namespace_prefix + '拉升通道', json.dumps(list(set([i for i in res['xuangu_tableV1']['股票代码']]))))
    # print_(res['xuangu_tableV1'])
    # print_data(res)
    # res = wc.get(query='市值小于100亿,剔除创业板股票,筹码集中度90小于15%,PE小于70,准备拉升')
    # print_('------------------------市值小于100亿,准备拉升----------------------------')
    # if res is not None: client.set(namespace_prefix + '近半年没有拉升过的', json.dumps(list(set([i for i in res['xuangu_tableV1']['股票代码']]))))
    # client.close()
    # print_(res['xuangu_tableV1'])
    # print_data(res)
    pass


# 用于处理队列中的消息的函数
def process_messages(message_queue):
    while True:
        # 从队列中取出消息
        # if not message_queue.empty():
        addr, data = message_queue.get()

        # 处理数据（这里简单地将数据原样发送回客户端）
        response = f"Received from {addr}: {data.decode('utf-8')}"


# 用于处理客户端连接的函数
def handle_client(client_socket, addr, message_queue):
    print_(f"Accepted connection from {addr}")

    while True:
        # 接收客户端数据
        data = client_socket.recv(1024)
        if not data:
            break
        print_(data.decode('gbk'))
        try:
            data = qs.intraday_data(data.decode('gbk')).tail(1).to_string()
        except Exception as e:
            print_(e)
            data = '无'
        print_(f'客户端发来:{data}')
        data_set = message_queue.get()
        print_(f'队列取出:{data_set}')
        print_(data_set)
        if data_set:
            client_socket.sendall(str(data_set).encode('gbk'))
        # 将数据放入队列

    # 关闭与客户端的连接
    client_socket.close()
    print_(f"Connection from {addr} closed")


def myServer(host, port):
    print_('myServer is running')

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    # 开始监听连接
    sock.listen()
    # 等待客户端连接
    while True:
        client_socket, client_address = sock.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address, message_queue))
        client_handler.start()


def myAnalyse(message_queue):
    print_('myAnalyse is running')
    stock_list = []
    while True:
        try:
            res = wc.get(query='市值小于50亿,即将启动拉升,剔除次新股,剔除st股,剔除创业板股票')
            if not res['xuangu_tableV1'].empty:
                print_(res)
            result_set = res['xuangu_tableV1'].loc[:, ['股票简称', '最新价', '股票代码', '所属同花顺行业', '准备拉升(条件说明)[20240110]', '技术形态[20240110]', '最新涨跌幅'], ]
            print_(result_set)
            da = res['xuangu_tableV1'].loc[:, ['股票简称']].values.ravel()
            [stock_list.append(i) for i in da]
        except Exception as e:
            print_(e)
        # data = qs.intraday_data('澳柯玛').tail(1)
        if not message_queue.empty():
            message_queue.queue.clear()
        message_queue.put(stock_list)
        print_(f'队列放入:{stock_list}')
        # for stock_name in stock_list:
        #     t.sleep(1)
        #     res = wc.get(query=f'{stock_name}最近30个交易日,股票开盘价和收盘价,最高价最低价成交量,散户数量,机构数量,大单数量,中单数量,小单数量,大单金额,中单金额,小单金额')
        #     print_(res)
        stock_list.clear()
        t.sleep(100)

def start_uvicorn():
    # 注意：这里的"main:app"意味着uvicorn会从main.py文件中寻找名为app的FastAPI实例
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")


if __name__ == '__main__':
    # analyse()
    message_queue = queue.Queue()
    brain_thread_list = []
    brain_thread_list.append(threading.Thread(target=brain_zgl, args=()))
    brain_thread_list.append(threading.Thread(target=wencai_, args=()))
    brain_thread_list.append(threading.Thread(target=start_uvicorn, args=()))
    # brain_thread_list.append(threading.Thread(target=myServer, args=("localhost", 8083,)))
    # brain_thread_list.append(threading.Thread(target=myAnalyse, args=(message_queue,)))

    for i in brain_thread_list:
        i.start()
