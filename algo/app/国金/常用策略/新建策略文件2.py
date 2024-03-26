# encoding:gbk
'''
本策略事先设定好交易的股票篮子，然后根据指数的CCI指标来判断超买和超卖
当有超买和超卖发生时，交易事先设定好的股票篮子
'''
import pandas as pd
import numpy as np
import talib
import os


def init(ContextInfo):
    print('策略开始')
    ContextInfo.set_account = '8881667160'


# hs300成分股中sh和sz市场各自流通市值最大的前3只股票


def handlebar(ContextInfo):
    print(os.getcwd())
# passorder(11)




