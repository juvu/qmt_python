#coding:gbk

import numpy as np
import pandas
import math
import time
import datetime
import scipy
from sklearn import linear_model

def init(ContextInfo):
	ContextInfo.stock = ContextInfo.stockcode + '.' + ContextInfo.market
	ContextInfo.set_universe([ContextInfo.stock])
	ContextInfo.HSIGMA = 0.0


def handlebar(ContextInfo):
	try:
		d = ContextInfo.barpos
		lastdate = timetag_to_datetime(ContextInfo.get_bar_timetag(d), '%Y%m%d')
		if d > 252:
			time_region = str(get_days_before_lastdate(lastdate, 252))
			ContextInfo.HSIGMA = getBeta(ContextInfo, lastdate, time_region)
		ContextInfo.paint('HSIGMA', ContextInfo.HSIGMA, -1, 0)
	except:
		pass

def getBeta(ContextInfo, lastdate, time_region):
	d = ContextInfo.barpos
	risk_free_list = []
	HS300_diff = []
	stock_diff = []
	last_date = str(get_days_before_lastdate(lastdate, 1))
	HS300_close = list(ContextInfo.get_market_data(fields=['close'],stock_code=["000300.SH"], end_time = lastdate, count = 252)['close'].values)
	HS300_last_close = list(ContextInfo.get_market_data(fields=['close'],stock_code=["000300.SH"], end_time = last_date, count = 252)['close'].values)
	target = ContextInfo.stockcode + "." + ContextInfo.market
	stock_close = list(ContextInfo.get_market_data(fields=['close'],stock_code=[target], end_time = lastdate, count = 252)['close'].values)
	stock_last_close = list(ContextInfo.get_market_data(fields=['close'],stock_code=[target], end_time = last_date, count = 252)['close'].values)

	for i in range(252):
		d_index = d - i
		if d_index<0:
			risk_free_list.append(0.00)
			HS300_diff.append(0.00)
			continue
		risk_free_list.append(ContextInfo.get_risk_free_rate(d_index))
		kk = float((HS300_close[i]-HS300_last_close[i])/HS300_last_close[i]) if (HS300_last_close[i] != 0.0  or not HS300_last_close[i]) else 1.00

		kk_stock = float((stock_close[i]-stock_last_close[i])/stock_last_close[i]) if (stock_last_close[i] != 0.0  or not stock_last_close[i]) else 1.00

		HS300_diff.append(kk)
		stock_diff.append(kk)
	Rt_Rft = []
	Rt_Rft = [float(stock_diff[i]-risk_free_list[i] / 100 / 365) for i in range(252)]
	half_lift = pow(0.5,1/ float(252))
	half_lift_list = [pow(half_lift,252 - i ) for i in range(252)]
	#print Rt_Rft
	#print half_lift_list
	Rt_Rft_series = np.array([a_b[0]*a_b[1] for a_b in zip(Rt_Rft, half_lift_list)]).reshape(252,1)
	HS300_diff_series = np.array([a_b1[0]*a_b1[1] for a_b1 in zip(HS300_diff, half_lift_list)]).reshape(252,1)
	lr = linear_model.LinearRegression()
	lr.fit(HS300_diff_series, Rt_Rft_series)
	Rt_Rft_predict = lr.predict(HS300_diff_series)
	e_std = np.std(np.array(Rt_Rft_predict))
	return e_std

def get_days_before_lastdate(lastdate, n=0):
	'''
	date format = "YYYY-MM-DD HH:MM:SS"
	'''
	last_date = datetime.datetime.strptime(lastdate, '%Y%m%d')
	if(n<0):
		return datetime.datetime(last_date.year, last_date.month, last_date.day, last_date.hour, last_date.minute, last_date.second)
	else:
		n_days_before = last_date - datetime.timedelta(days=n)
	return datetime.datetime(n_days_before.year, n_days_before.month, n_days_before.day).strftime('%Y%m%d')