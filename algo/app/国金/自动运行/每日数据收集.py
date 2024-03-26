# encoding:gbk
'''
本策略事先设定好交易的股票篮子，然后根据指数的CCI指标来判断超买和超卖
当有超买和超卖发生时，交易事先设定好的股票篮子
'''
import pandas as pd
import numpy as np
import talib


def init(ContextInfo):
    # hs300成分股中sh和sz市场各自流通市值最大的前3只股票
    ContextInfo.trade_code_list = ['601398.SH', '601857.SH', '601288.SH', '000333.SZ', '002415.SZ', '000002.SZ']
    ContextInfo.set_universe(ContextInfo.trade_code_list)
    ContextInfo.accID = '6000000058'
    ContextInfo.buy = True
    ContextInfo.sell = False


def handlebar(ContextInfo):
    if not ContextInfo.is_last_bar():
        return
    Result = ContextInfo.get_full_tick(['601398.SH', '601857.SH', '601288.SH', '000333.SZ', '002415.SZ', '000002.SZ'])
    df = pd.DataFrame(Result)
    df2 = df.T
    df2.to_csv('24-02-05.csv', mode='a', header=None)
    print('写入成功!')



