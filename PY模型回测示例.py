#coding:gbk
#!/usr/bin/python
import time, datetime
import numpy as np

#上证50指数，建议本模型在上证指数日线周期下跑

def init(ContextInfo):
	#取成份股
	s=ContextInfo.get_stock_list_in_sector('上证50')
	#print s
	
	#设置股票池
	ContextInfo.set_universe(s)
	
	#设置基准(当前图给基准)
	ContextInfo.benchmark=ContextInfo.stockcode+"."+ContextInfo.market
	
	ContextInfo.tmp = {i:0 for i in s}
	
def handlebar(ContextInfo):
	d = ContextInfo.barpos
	realtime = ContextInfo.get_bar_timetag(d)
	nowdate = timetag_to_datetime(realtime,'%Y-%m-%d')
	#输出当前运行到的日期
	print(nowdate)
	ContextInfo.holdings=get_holdings('testS','STOCK')
	last20s=ContextInfo.get_history_data(21,'1d','close')
	count=0
	buyNumber = 0
	buyAmount = 0
	sellNumber = 0
	sellAmount = 0
	for k ,closes in list(last20s.items()):
		if len(closes)<21:
			continue
		pre=closes[-1]
		m20=np.mean(closes[:20])
		m5=np.mean(closes[-6:-1])
		
		if ContextInfo.tmp[k] == 0:
			if m5 >= m20:
				ContextInfo.tmp[k] = 0
			else:
				ContextInfo.tmp[k] = 1
		else:
			#对股票池中满足条件的股票进行买卖
			if m5 <= m20:
				if k in ContextInfo.holdings:
					sellNumber += 1
					sellAmount += float(ContextInfo.holdings[k]) * pre
					order_shares(k,-float(ContextInfo.holdings[k]),"FIX",pre,ContextInfo,"testS")
					del ContextInfo.holdings[k]
					print('卖出%s'%k)

				
			else:
				if  k not in ContextInfo.holdings:
					ContextInfo.holdings[k] = 500
					buyNumber += 1
					buyAmount += float(ContextInfo.holdings[k]) * pre
					order_shares(k,float(ContextInfo.holdings[k]),"FIX",pre,ContextInfo,"testS")
					print('买入%s'%k)
	ContextInfo.paint("buy_num", buyNumber, -1, 0)
	ContextInfo.paint("sell_num", sellNumber, -1, 0)
					
def get_holdings(accountid,datatype):
	holdinglist={}
	resultlist=get_trade_detail_data(accountid,datatype,"POSITION")
	for obj in resultlist:
		holdinglist[obj.m_strInstrumentID+"."+obj.m_strExchangeID]=obj.m_nVolume
	return holdinglist


