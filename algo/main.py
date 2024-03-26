import datetime
import os.path
import threading
import time

import logging

import efinance as ef
import pywencai as wc
import pandas as pd
import easyquotation

import logging

logging.basicConfig(
    level=logging.NOTSET,
    filename='./default.log'
)

quotation = easyquotation.use('tencent')  # 新浪 ['sina'] 腾讯 ['tencent', 'qq']
# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
# pd.set_option('display.width', 1000)
# pd.set_option('display.unicode.ambiguous_as_wide', True)
# pd.set_option('display.unicode.east_asian_width', True)
# pd.set_option('display.width', 180)  # 设置打印宽度(**重要**)
import datetime
import webbrowser

# create database
now = datetime.datetime.now()
day = now.strftime("%Y-%m-%d")

from sqlalchemy import create_engine

def print_(str):
    print(str)
    logging.log(logging.INFO,str)

# engine = create_engine('postgresql://postgres:123456@localhost:5432/test')

def print__data(res):
    if res is None: return
    print_(res)
    try:
        res.rename(columns={'股票简称': 'name', '最新价': 'price'}, inplace=True)
        res.sort_values(by='code', ascending=True, inplace=True, )
        res = res.loc[:, ['code', 'name', 'price']].drop_duplicates()
        for row in res.iterrows():
            try:
                result_set = wc.get(query=row[1]['name'], )
                df3 = pd.merge(result_set['barline3'], result_set['历史主力资金流向']['barline3'])

                # print__demo(result_set['近期重要事件'])
                # print_(result_set['所属概念列表']['诊股概念分类名称'].to_list())
                # print_("-" * 100)
                # print_(f"支撑位:{result_set['kline2'].iloc[0:]['止盈止损(支撑位)'][0]} ------压力位:{result_set['kline2'].iloc[0:]['止盈止损(压力位)'][0]}----{result_set['支撑位压力位']}")
                # if '若能站稳，意味着上涨空间打开，可适当关注5日均线，若跌破可考虑止盈' in result_set['支撑位压力位']:
                # print_(result_set['财务数据'])
                # print_(result_set['估值指标']['市净率']['txt1'][40:])
                # print_(result_set['估值指标']['市销率']['txt1'][52:])
                # print_(result_set['十大股东持股比例'].loc[:, ['大股东名称', '大股东持股比例', '大股东公告日期', '股东类型']])
                # result_set['估值指标']['市销率']['labelLine'].tail(30)           # 有参考价值
                # result_set['估值指标']['市净率']['labelLine'].tail(30)           # 有参考价值
                # result_set['估值指标']['市净率']['labelLine'].tail(30)           # 有参考价值
                # result_set['barline3']
                # result_set['所属概念列表']
                # result_set['历史主力资金流向']['barline3']
                # result_set['kline2']
                # result_set['估值指标']['市盈率']['labelLine']
                # result_set['估值指标']['市净率']['labelLine']
                # result_set['估值指标']['市销率']['labelLine']
                # print_(df3)
                # else:
                #     pass
                # print_(df3)
                print_(df3)
            except Exception as e:
                print_(e)
    except Exception as e:
        print_(e)
    if res is not None and 'code' in res.columns:
        return res['code'].to_list()


def code_list_to_csv(code_list: list):
    """
    将股票代码列表转换为csv文件
    """
    if not os.path.exists(f'./data/{day}'):
        os.makedirs(f'./data/{day}')
    if code_list:
        freq = 1
        for i in code_list:
            df = ef.stock.get_quote_history(i, klt=freq)
            df.to_csv(f'./data/{day}/{i}.csv', encoding='utf-8-sig', index=None)


def question_wc(question):
    res = None
    try:
        res = wc.get(query=question)
    except Exception as e:
        webbrowser.open('https://www.iwencai.com/unifiedwap/reptile.html?returnUrl=https%3A%2F%2Fwww.iwencai.com%2Funifiedwap%2Fhome%2Findex%3Fsign%3D1709793871013&sessionId=117.30.119.18&antType=unifiedwap')
        print_(e)
        time.sleep(20)
    if res is not None:
        res_list = print__data(res)
        code_list_to_csv(res_list)
        return res_list
    return None


# 用于处理队列中的消息的函数
# 竞价策略
# 百度查这个 ：集合竞价怎么选股
# res = wc.get(query=)

# https://zhuanlan.zhihu.com/p/370195994#:~:text=%E2%80%9C%E9%9B%86%E5%90%88%E7%AB%9E%E4%BB%B7%E6%89%93%E6%9D%BF%E2%80%9D%E8%BD%BB%E6%9D%BE%E9%80%89%E5%87%BA%E6%B6%A8%E5%81%9C%E8%82%A1%20%28%E5%86%85%E9%99%84%E6%8C%87%E6%A0%87%E6%BA%90%E7%A0%81%29%201%20%E4%B8%89%E7%A7%8D%E5%85%B8%E5%9E%8B%E8%B5%B0%E5%8A%BF%EF%BC%8C%E7%9C%8B%E6%87%82%E9%9B%86%E5%90%88%E7%AB%9E%E4%BB%B7%E7%9A%84%E6%89%93%E6%9D%BF%E7%AD%96%E7%95%A5%20%E5%AF%B9%E5%A4%A7%E8%B5%84%E9%87%91%E8%80%8C%E8%A8%80%EF%BC%8C%E9%9B%86%E5%90%88%E7%AB%9E%E4%BB%B7%E6%98%AF%E5%85%A8%E5%A4%A9%E6%93%8D%E7%9B%98%E6%B4%BB%E5%8A%A8%E7%9A%84%E5%BA%8F%E5%B9%95%EF%BC%8C%E5%A4%9A%E7%A9%BA%E5%8F%8C%E6%96%B9%E7%BB%8F%E5%B8%B8%E5%9C%A8%E8%BF%99%E6%97%B6%E8%BF%9B%E8%A1%8C%E7%AC%AC%E4%B8%80%E8%BD%AE%E6%83%A8%E7%83%88%E5%8E%AE%E6%9D%80%E3%80%82%20%E5%9C%A8%E8%BF%9915%E5%88%86%E9%92%9F%E9%87%8C%EF%BC%8C%E5%BE%80%E5%BE%80%E4%BC%9A%E4%BD%93%E7%8E%B0%E5%A4%A7%E8%B5%84%E9%87%91%E6%97%A5%E5%86%85%E7%9A%84%E5%81%9A%E7%9B%98%E6%84%8F%E5%9B%BE%E3%80%82%20...%202,%E7%AC%AC%E4%B8%89%E7%A7%8D%EF%BC%8C%E6%A8%AA%E7%9B%98%E8%B5%B0%E9%AB%98%E3%80%82%20%E6%8C%87%E7%9A%84%E6%98%AF9%3A20%E4%B9%8B%E5%90%8E%EF%BC%8C%E6%92%AE%E5%90%88%E4%BB%B7%E6%A0%BC%E7%A8%B3%E5%AE%9A%E4%B8%8D%E5%8A%A8%EF%BC%8C%E7%AB%9E%E4%BB%B7%E8%BD%A8%E8%BF%B9%E5%91%88%E4%B8%80%E6%9D%A1%E7%9B%B4%E7%BA%BF%20%28%E5%A4%A7%E8%B5%84%E9%87%91%E6%8E%A7%E7%9B%98%29%EF%BC%8C%E6%9C%80%E7%BB%88%E7%AB%9E%E4%BB%B7%E5%B0%8F%E5%B9%85%E9%AB%98%E5%BC%80%E6%88%96%E5%B9%B3%E5%BC%80%E3%80%82%20...%205%20%E6%9C%80%E5%90%8E%EF%BC%8C%E5%86%8D%E9%80%81%E5%A4%A7%E5%AE%B6%E4%B8%80%E4%B8%AA%E9%80%9A%E8%BE%BE%E4%BF%A1%E9%9B%86%E5%90%88%E7%AB%9E%E4%BB%B7%E9%80%89%E8%82%A1%E5%85%AC%E5%BC%8F%EF%BC%9A%20%7B9%E7%82%B925%E5%88%86-9%E7%82%B929%E5%88%86%E9%80%89%E8%82%A1%7D%20


def watch(code_list: list):
    print_('观察线程已经启动')
    print_(code_list)
    while True:
        try:
            print_(quotation.stocks(code_list, prefix=True))
            time.sleep(60)
        except Exception as e:
            print_(e)
            time.sleep(60)
    
def watch_market():
    print_('thread watch_market is runing')
    
    
threading.Thread(target=watch_market, args=()).start()


question_list = [
    '市值小于50亿,剔除ST,缩量,最近10个交易日有6个交易日以上主力资金净流入,最近3个交易日涨幅为正,资金净流入的股票,散户买入,筹码高度集中,MACD大于0,',
    '散户持续买入,放量,剔除ST,剔除次新,亿剔除次北交所,最近10个交易日有6个交易日以上主力资金净流入,最近3个交易日涨幅为正,筹码高度集中,MACD大于0,业绩预增大于20%',
    '放量,不包括次新股,剔除ST,剔除次新,亿剔除次北交所,股票市场不包括北交所,散户持续买入,筹码高度集中,MACD大于0,',
    '市值小于50亿,放量,剔除ST,剔除次新,剔除北交所,拉升通道',
    '市值小于100亿,亿剔除次新股,拉升通道,股票市场只包括创业板,散户持续买入,MACD大于0,',
    '市值小于100亿,拉升,仅创业板,剔除ST,散户持续买入,MACD大于0,',
    '9:20之前的竞价出现涨跌停价挂单加分,剔除ST',
    '9:20~9:25期间，撮合价格逐步走高，同时伴随着成交量的放大，且以密集红柱为主。最好在最后一两分钟内 有快速拉高(大资金强吃货)，且最终竞价涨幅在3%~7%之间',
    '9:30前，有巨单挂过涨跌停价,个股形态完好，前几日分时有过异动或者有过涨停,开始股价涨停 ，竞价过程中撮合价格慢慢走低，但成交量有效放大，并且承接很好，主买盘为主'
]

watch_list = []
for i in question_list:
    res = question_wc(i)            # 返回需要观察的股票代码
    if res is not None:
        print_(res)
        watch_list = watch_list + res
        print_(quotation.stocks(res, prefix=True))


threading.Thread(target=watch, args=(watch_list,)).start()

