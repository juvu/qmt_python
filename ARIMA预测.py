#encoding:gbk
# close_5 是今天的收盘价，close_predict5是五天前预测的今天的收盘价，预测失败则取五天前的收盘价

import pandas as pd
import numpy as np
import statsmodels.api as sm
import warnings


def init(ContextInfo):
	print('init初始设定函数,无设定则直接pass')
	warnings.filterwarnings('ignore')
	pass

def handlebar(ContextInfo):
	#handlebar 逐跟K线调用运行函数

	#当前K线的对应的下标从0开始
	index = ContextInfo.barpos
	print(index)
	if index < 250:
		return
	#当前K线对应的时间：毫秒
	realtime = ContextInfo.get_bar_timetag(index)
	
	#五天前日期
	date_5 = timetag_to_datetime(ContextInfo.get_bar_timetag(index-5),"%Y%m%d")
	#当前周期
	period = ContextInfo.period
	
	#当前主图复权方式
	dividend_type = ContextInfo.dividend_type
	
	#取当前K线图对应的合约当前K线的当前主图复权方式下的收盘价
	close = ContextInfo.get_market_data(['close'],period=period,dividend_type=dividend_type,count=240)

	
	try: 
		closedata = np.array(close.diff(periods=3)["close"]) # 收盘价的ADF检验
		if ContextInfo.is_last_bar():
			closedata_0 = closedata[3:-4]
			closedataModel_ARIMA = sm.tsa.ARMA(closedata_0,(4,3)).fit()
			predicts_ARIMA = closedataModel_ARIMA.predict(232, 241, dynamic = True)
			print("预测后五天的价格",predicts_ARIMA[0]+close["close"][-1],predicts_ARIMA[1]+close["close"][-1], \
			predicts_ARIMA[2]+close["close"][-1],predicts_ARIMA[3]+close["close"][-1],\
			predicts_ARIMA[4]+close["close"][-1])
		closedata_5 = closedata[3:-4]
		#print len(closedata)
		#adftest = sm.tsa.stattools.adfuller(closedata)
		
		#if adftest[1] > 0.001:
			#return
		#result = sm.tsa.arma_order_select_ic(closedata,max_ar=6,max_ma=4,ic='aic')['aic_min_order']
		#print result

		closedataModel_ARIMA = sm.tsa.ARMA(closedata_5,(4,3)).fit()
		#print closedataModel_ARIMA.fittedvalues
		
		predicts_ARIMA = closedataModel_ARIMA.predict(232, 241, dynamic = True)
		#print predicts_ARIMA[4]
		ContextInfo.paint("close_5", close["close"][-1],-1,0)
		ContextInfo.paint("close_predict5", predicts_ARIMA[4]+close["close"][-5],-1,0)
		
		
		predicts_ARIMA = closedataModel_ARIMA.predict(232, 241, dynamic = True)
	except:
		ContextInfo.paint("close_5", close["close"][-1],-1,0)
		ContextInfo.paint("close_predict5", close["close"][-5],-1,0)
		print("预测失败")
