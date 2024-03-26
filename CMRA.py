#coding:gbk

import numpy as np
import pandas
import math

def init(ContextInfo):
	ContextInfo.stock = ContextInfo.stockcode + '.' + ContextInfo.market
	print("ContextInfo.stock", ContextInfo.stock)
	ContextInfo.set_universe([ContextInfo.stock])
	ContextInfo.month = '00'
	ContextInfo.CMRA = 0

def handlebar(ContextInfo):
	d = ContextInfo.barpos
	lastdate = timetag_to_datetime(ContextInfo.get_bar_timetag(d - 1), '%Y%m%d')
	date = timetag_to_datetime(ContextInfo.get_bar_timetag(d), '%Y%m%d')
	if date[4:6] != ContextInfo.month:
		ContextInfo.month = date[4:6]
	else:
		ContextInfo.paint('CMRA', ContextInfo.CMRA, -1, 0)
		return

	Zt_list = []
	origin_data = get_last_12_month_data(date, 'close', ContextInfo)
	if origin_data.empty:
		return

	for i in range(12):
		try:
			Zt_list.append(calc_zt(i + 1, origin_data, ContextInfo))
		except:
			return

	ZMax = max(Zt_list)
	ZMin = min(Zt_list)
	try:
		ContextInfo.CMRA = math.log((1+ZMax) / (1+ZMin))
	except:
		print((1+ZMax) , (1+ZMin))
		print('value error!')
	ContextInfo.paint('CMRA', ContextInfo.CMRA, -1, 0)

def calc_zt(month, origin_data, ContextInfo):
	sumReturn = 0
	sumRiskFreeReturn = 0
	start_pos = ContextInfo.barpos - 12 * 23
	for i in range(month):
		t = i + 1
		start_index = int(origin_data.size / 12 * (t-1))
		end_index = int(origin_data.size / 12 * t)
		Return = origin_data.values[end_index-1][0] / origin_data.values[start_index][0] - 1
		tmp = math.log(1 + Return)
		sumReturn += tmp
		riskFree = ContextInfo.get_risk_free_rate(start_pos + i * 23)
		if riskFree <= 0:
			riskFree = 3.5
		riskFree = riskFree / 100 / 12
		#print riskFree
		tmp_rf = math.log(1 + riskFree)
		sumRiskFreeReturn += tmp_rf


	return sumReturn - sumRiskFreeReturn

def get_last_12_month_data(date, strtype, ContextInfo):
	time_region = get_last_12_month_date_region(date)
	price = ContextInfo.get_market_data([strtype],stock_code=[ContextInfo.stock],start_time=time_region[0],end_time=time_region[1],period='1d')
	if price.empty:
		print('data is empty!')
		return price
	else:
		tailDate = price.tail(1).index[0]
		if tailDate[6:] == '01':
			noTailData = price.drop(tailDate)
			return noTailData
		else:
			return price

def get_last_12_month_date_region(date):
	end_date = month_start_date(date)
	last_year = str(int(end_date[:4]) - 1)
	start_date = last_year + end_date[4:]
	return start_date, end_date

def month_start_date(cur_date):
	return cur_date[:6] + '01'