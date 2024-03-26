#coding:gbk

import numpy as np
import pandas
import math
import time
import datetime

def init(ContextInfo):
	ContextInfo.stock = ContextInfo.stockcode + '.' + ContextInfo.market
	ContextInfo.set_universe([ContextInfo.stock])
	print(ContextInfo.stock)
	ContextInfo.month = '00'
	ContextInfo.STOQ = 0.0


def handlebar(ContextInfo):
	try:
		d = ContextInfo.barpos
		lastdate = timetag_to_datetime(ContextInfo.get_bar_timetag(d - 1), '%Y%m%d')
		date = timetag_to_datetime(ContextInfo.get_bar_timetag(d), '%Y%m%d')
		total_stom = 0.0
		for i in range(3):
			d_index = d-i*21
			per_date = timetag_to_datetime(ContextInfo.get_bar_timetag(d_index), '%Y%m%d')
			per_stom = get_STOM(ContextInfo, per_date, d_index)
			total_stom += math.exp(per_stom)
		ContextInfo.STOQ = math.log(float(total_stom/3))
	except:
		pass
	ContextInfo.paint('STOQ', ContextInfo.STOQ, -1, 0)

def get_STOM(ContextInfo, lastdate, d_index):
	time_region = str(get_days_before_lastdate(lastdate, 35))
	vt_list = ContextInfo.get_market_data(fields=['volume'],stock_code=[ContextInfo.stock],start_time=time_region,end_time=lastdate)
	vt_list_index_reverse = vt_list.index.tolist()
	vt_list_index_reverse.reverse()
	stom_total = 0.0
	for index_i in range(21):
		circulating_capital = ContextInfo.get_financial_data('CAPITALSTRUCTURE','circulating_capital',ContextInfo.market,ContextInfo.stockcode, d_index-index_i)
		if circulating_capital :
			stom_total += float(vt_list['volume'][vt_list_index_reverse[index_i]] / circulating_capital)
	return stom_total


def get_days_before_lastdate(lastdate, n=0):
	'''
	date format = "YYYY-MM-DD HH:MM:SS"
	'''
	last_date = datetime.datetime.strptime(lastdate, '%Y%m%d')
	if(n<0):
		return datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, now.second)
	else:
		n_days_before = last_date - datetime.timedelta(days=n)
	return datetime.datetime(n_days_before.year, n_days_before.month, n_days_before.day).strftime('%Y%m%d')