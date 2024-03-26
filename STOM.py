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
	ContextInfo.STOM = 0.0


def handlebar(ContextInfo):
	try:
		d = ContextInfo.barpos
		date = timetag_to_datetime(ContextInfo.get_bar_timetag(d), '%Y%m%d')
		time_region = str(get_days_before_lastdate(date, 35))
		vt_list = ContextInfo.get_market_data(fields=['volume'],stock_code=[ContextInfo.stock],end_time=date, count = 21)
		vt_list_index_reverse = vt_list.index.tolist()
		vt_list_index_reverse.reverse()
		vt_list_array = [vt_list['volume'][vt_list_index_reverse[k]] for k in range(21)]
		circulating_capital_frame = ContextInfo.get_financial_data(['CAPITALSTRUCTURE.circulating_capital'], [ContextInfo.stock],time_region,date)
		cc_list_index_reverse = circulating_capital_frame.index.tolist()
		cc_list_index_reverse.reverse()
		cc_list_array = [circulating_capital_frame['circulating_capital'][cc_list_index_reverse[k]] for k in range(21)]
		total_stom = 0.0
		for i in range(21):
			if cc_list_array[i] != 0.0:
				total_stom += vt_list_array[i] / cc_list_array[i]
		ContextInfo.STOM = math.log(float(total_stom))
	except:
		pass
	ContextInfo.paint('STOM', ContextInfo.STOM, -1, 0)

def get_STOM(ContextInfo, vt_list_one=[], cc_list_one=[]):
	stom_total = 0.0
	for i in range(21):
		if cc_list_one[i] :
			stom_total += float(vt_list_one[i] / cc_list_one[i])
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