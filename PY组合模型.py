#coding:gbk
#HS300日线下运行
#股票池暂设为包含4只股票，每只分配可用资金的25%
import pandas as pd
import numpy as np
import time
import datetime

s = ['600000.SH','600004.SH','000001.SZ','000002.SZ']            #股票池
def init(ContextInfo):
	ContextInfo.set_universe(s)
	ContextInfo.day = 0
	ContextInfo.weight = [0.25,0.25,0.25,0.25]         #设置初始权重
	ContextInfo.money_distribution_original = {k:i*ContextInfo.capital for (k,i) in zip(s,ContextInfo.weight)}
	ContextInfo.money_distribution = ContextInfo.money_distribution_original
	ContextInfo.buypoint = {}
	ContextInfo.accountID='testS'

def handlebar(ContextInfo):
	d = ContextInfo.barpos
	timetag = ContextInfo.get_bar_timetag(d)
	ContextInfo.holdings = get_holdings(ContextInfo.accountID,"STOCK")
	if ContextInfo.day == 0:
		ContextInfo.benchmark_start = ContextInfo.get_market_data(['close'],period='1d')
	benchmark = ContextInfo.get_market_data(['close'],period='1d')
	#print benchmark
	net_hs300 = benchmark/ContextInfo.benchmark_start
	ContextInfo.paint('沪深300指数净值',net_hs300,-1,0)
	ContextInfo.paint('沪深300指数收益',net_hs300-1,-1,0)
	tmp = ContextInfo.get_history_data(1,'1d','open',3)
	if d > 60:
		nowDate = timetag_to_datetime(ContextInfo.get_bar_timetag(d),'%Y%m%d')
		print(nowDate)
		buys, sells = signal(ContextInfo)
		order = {}
		for k in s:
			if k not in ContextInfo.holdings and buys[k] == 1:              #在买入备选中且无持仓
				print('ready to buy',k)
				order[k] = int(ContextInfo.money_distribution[k]/(tmp[k][-1]))/100
				order_shares(k,order[k]*100,'fix',tmp[k][-1],ContextInfo,ContextInfo.accountID)
				ContextInfo.buypoint[k] = tmp[k][-1]
				ContextInfo.money_distribution[k] -= 0.0003*order[k]*100*tmp[k][-1]
				#print ContextInfo.money_distribution[k]
			elif k in ContextInfo.holdings and sells[k] == 1:           #在卖出备选中且有持仓
				print('ready to sell',k)
				order_shares(k,-ContextInfo.holdings[k]*100,'fix',tmp[k][-1],ContextInfo,ContextInfo.accountID)
				ContextInfo.money_distribution[k] += (tmp[k][-1]-ContextInfo.buypoint[k]) * ContextInfo.holdings[k] * 100 - 0.0003*ContextInfo.holdings[k]*100*tmp[k][-1]
				#print tmp[k][-1]
				#print ContextInfo.buypoint[k]
				#print ContextInfo.money_distribution[k]
		profit = sum(ContextInfo.money_distribution.values())/ContextInfo.capital - 1
		ttt = 0
		for v in list(ContextInfo.holdings.values()):
			if v > 0:
				ttt += 1
		ContextInfo.paint('收益',profit,-1,0)
		ContextInfo.paint('对冲收益',profit-net_hs300-1,-1,0)
		ContextInfo.paint('对冲收益净值',profit+1-net_hs300,-1,0)
		ContextInfo.paint('个股',ttt,-1,0)
		ContextInfo.day += 1
		
def signal(ContextInfo):
	buy = {i:0 for i in s}
	sell = {i:0 for i in s}
	data_high = ContextInfo.get_history_data(22,'1d','high',3)
	data_high_pre = ContextInfo.get_history_data(2,'1d','high',3)
	data_close60 = ContextInfo.get_history_data(62,'1d','close',3)
	#print data_high
	#print data_close
	#print data_close60
	for k in list(data_high_pre.keys()):
		if k in data_close60:
			if len(data_high_pre[k]) == 2 and len(data_high[k]) == 22 and len(data_close60[k]) == 62:
				if data_high_pre[k][-2] > max(data_high[k][:-2]):
					buy[k] = 1               #超过20日最高价，加入买入备选
				elif data_high_pre[k][-2] < np.mean(data_close60[k][:-2]):
					sell[k] = 1              #低于60日均线，加入卖出备选
	#print buy
	#print sell
	return buy,sell             #买入卖出备选

def get_holdings(accountid,datatype):
	holdinglist={}
	resultlist=get_trade_detail_data(accountid,datatype,"POSITION")
	for obj in resultlist:
		holdinglist[obj.m_strInstrumentID+"."+obj.m_strExchangeID]=obj.m_nVolume/100
	return holdinglist

