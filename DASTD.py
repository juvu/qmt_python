#coding:gbk

import numpy as np
import math



def init(ContextInfo):
	ContextInfo.stock = ContextInfo.stockcode + '.' + ContextInfo.market
	ContextInfo.set_universe([ContextInfo.stock])

def handlebar(ContextInfo):
	d = ContextInfo.barpos
	lastdate = timetag_to_datetime(ContextInfo.get_bar_timetag(d - 1), '%Y%m%d')
	date = timetag_to_datetime(ContextInfo.get_bar_timetag(d), '%Y%m%d')

	stock_last_2_close = ContextInfo.get_history_data(252,'1d','close')
	if ContextInfo.stock in stock_last_2_close:
		if len(stock_last_2_close[ContextInfo.stock]) != 252:
			return
	else:
		return
	#rf = ContextInfo.get_risk_free_rate()
	#if rf <= 0:
	#	rf = 3.5
	#rf = rf / 100 / 365
	stock_value = stock_last_2_close[ContextInfo.stock]
	stock_r = [stock_value[i + 1] / stock_value[i] for i in range(250)]
	stock_mean_r = sum(stock_r) / len(stock_r)
	stock_var = 0
	half_lift = pow(0.5,1/ float(252))
	half_lift_list = [pow(half_lift, 250-i) for i in range(250)]
	for i in range(len(stock_r)):
		stock_var +=half_lift_list[i] * (stock_r[i] - stock_mean_r) ** 2
	stock_std = stock_var ** 0.5
	print("std", stock_std)
	ContextInfo.paint('DASTD', stock_std, -1, 0)