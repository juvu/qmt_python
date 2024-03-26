# encoding:gbk
'''
本策略事先设定好交易的股票篮子，然后根据指数的CCI指标来判断超买和超卖
当有超买和超卖发生时，交易事先设定好的股票篮子
'''
import pandas as pd
import numpy as np
import talib
import redis

client = redis.Redis(host='localhost', port=6379, db=1, password='123456')
namespace_prefix = 'data:'
print("策略启动")
# data = get_market_data(['open','close','volume','high','low','amount'],stock_code=['300056.SZ'],start_time='2006-1-1',period='1d',dividend_type='none',count=500)
# print(data)
def init(ContextInfo):
    # ContextInfo.capital = 10000000
    account = '8881667160'
    commissionList = [0, 0.0001, 0.0003, 0.0003, 0, 5]  # 手续费
    # hs300成分股中sh和sz市场各自流通市值最大的前3只股票
    # ContextInfo.trade_code_list = ['601398.SH', '601857.SH', '601288.SH', '000333.SZ', '002415.SZ', '000002.SZ']
    # ContextInfo.set_universe(ContextInfo.trade_code_list)
    ContextInfo.accID = account
    # 设定买入印花税为 0，卖出印花税为 0.0001，开仓手续费和平仓（平昨）手续费均为万三，平今手续费为 0，最小手续费为 5
    # ContextInfo.set_commission(0, commissionList)
    # ContextInfo.start = '2023-12-06 10:00:00'
    # ContextInfo.end = '2023-12-08 14:30:00'
    # data = ContextInfo.get_market_data_ex(
    #     fields=['close'],
    #     stock_code=['000001.SZ'],
    #     period='1d',
    #     dividend_type='front')
    # print(data)


def handlebar(ContextInfo):
    print(ContextInfo.capital)
    print(ContextInfo.get_universe())
    print(ContextInfo.period)
    print(ContextInfo.barpos)
    print(ContextInfo.time_tick_size)  # 获取当前图 K 线数目
    print(ContextInfo.is_last_bar())  # 判定是否为最后一根 K 线
    print(ContextInfo.is_new_bar())  # 判定是否为新的 K 线
    print(ContextInfo.is_suspended_stock('600004.SH'))  # 判定股票是否停牌
    # print(is_sector_stock('沪深300', 'SH', '600000'))  # 判定给定股票代码是否在指定的板块中
    # print(ContextInfo.do_back_test)  # 表示当前是否开启回测模式
    # index = ContextInfo.barpos
    # print(get_result_records('buys', index, ContextInfo))  # 获取某个记录类型对应的某个时刻的记录情况
	# # 综合交易下单
	# passorder(23,1101,"test",'601398.SH',5,-1,100,ContextInfo)








