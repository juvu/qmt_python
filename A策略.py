#coding:gbk
#By ZhangDegao,RZRK,20180102
import time, datetime
import numpy as np

moneybase=1000000

def init(ContextInfo):
	holdings={}
	ContextInfo.holdings=holdings
	ContextInfo.money=moneybase
	ContextInfo.buypoint = 0      #买入之后的涨跌价格
	ContextInfo.hs300bp = 0             #买入时的HS300指数
	ContextInfo.thisprofit = 0
	ContextInfo.hstmp = 0
	ContextInfo.hszhishu = 0
	ContextInfo.zhishu = 0
	ContextInfo.tmp = 0
	ContextInfo.profit = 0
	ContextInfo.DCS = 0
	ContextInfo.HSthisprofit = 0
	ContextInfo.value = []
	ContextInfo.HoldingTime = 0
	ContextInfo.TestHolding = 0
	ContextInfo.BuyTime = 0
	ContextInfo.TradeTime = 0
	ContextInfo.valuerange = []
	ContextInfo.hedge = []
	ContextInfo.hedgerange =[]
	s=[ContextInfo.stockcode+'.'+ContextInfo.market]
	#print s
	ContextInfo.set_universe(s)
	ContextInfo.count=0
	ContextInfo.HoldCircle = 0#持仓周期
	ContextInfo.zst = 0
	ContextInfo.CJt = []
	ContextInfo.dcCJt = []
	ContextInfo.cjt1 = 0
	ContextInfo.qzzhishu = []
	ContextInfo.qzdczhishu = []
	ContextInfo.perioddic = {'1d':86400000,'1m':60000,'5m':300000,'15m':900000,'30m':1800000,'60m':3600000}
	
def handlebar(ContextInfo):
	d = ContextInfo.barpos
	print(d)
	now=ContextInfo.get_bar_timetag(d)
	ContextInfo.count+=1
	print("here",ContextInfo.count)
	print("="*10)
	money=ContextInfo.money
	investment=0
	currentperiod = ContextInfo.period
	last60s=ContextInfo.get_history_data(60,currentperiod,'close',0)
	print(len(last60s))
	last=ContextInfo.get_history_data(2,currentperiod,'open',0)
	for k ,opens in list(last.items()):
		if len(opens)<2:
			continue
		pre_open = opens[-1]
	count=0
	
	if ContextInfo.BuyTime > 0 :
		ContextInfo.HoldCircle = d - ContextInfo.BuyTime 
		#ContextInfo.HoldCircle += 1
		#print '持仓周期',ContextInfo.HoldCircle
	else:
		ContextInfo.HoldCircle = 0
	#ContextInfo.paint('持仓周期',ContextInfo.HoldCircle,d,0,'noaxis')
	
	last = ContextInfo.get_bar_timetag(d - ContextInfo.HoldCircle)
	
	hs300c = ContextInfo.get_close_price("SH","000300",now,ContextInfo.perioddic[currentperiod])
	hs300c_HoldCircle = ContextInfo.get_close_price("SH","000300",last,ContextInfo.perioddic[currentperiod])
	ContextInfo.zst = (hs300c - hs300c_HoldCircle)/hs300c_HoldCircle
	#ContextInfo.paint('zst',ContextInfo.zst,d,0,'noaxis')   #持仓期间指数涨跌幅
	
	c = ContextInfo.get_close_price(ContextInfo.market,ContextInfo.stockcode,now,ContextInfo.perioddic[currentperiod])
	c_HoldCircle = ContextInfo.get_close_price(ContextInfo.market,ContextInfo.stockcode,last,ContextInfo.perioddic[currentperiod])
	ContextInfo.ggt = (c - c_HoldCircle)/c_HoldCircle
	#ContextInfo.paint('ggt',ContextInfo.ggt,d,0,'noaxis')
	
	ContextInfo.CJt.append(1*ContextInfo.ggt)
	#if len(ContextInfo.CJt):
		#ContextInfo.paint('CJt',ContextInfo.CJt[-1],d,0,'noaxis')   #/计算纯多头实时收益
	
	ContextInfo.dcCJt.append(1 * (ContextInfo.ggt - ContextInfo.zst))
	#if len(ContextInfo.dcCJt):
		#ContextInfo.paint('dcCJt',ContextInfo.dcCJt[-1],d,0,'noaxis')#计算对冲实时收益
		
	if len(ContextInfo.CJt)>2:
		cjt_refcjt= ContextInfo.CJt[-1] - ContextInfo.CJt[-2]
	else:
		cjt_refcjt = 0
	if ContextInfo.TestHolding > 0:
		ContextInfo.cjt1 = cjt_refcjt * 100
	else :
		ContextInfo.cjt1 = 0 
	#ContextInfo.paint('cjt1',ContextInfo.cjt1,d,0,'noaxis')#每个周期的多头收益
	
	if len(ContextInfo.dcCJt)>2:
		dccjt_refdccjt= ContextInfo.dcCJt[-1] - ContextInfo.dcCJt[-2]
	else:
		dccjt_refdccjt = 0
	if ContextInfo.TestHolding > 0:
		ContextInfo.dccjt1 = dccjt_refdccjt * 100
	else :
		ContextInfo.dccjt1 = 0 
	#ContextInfo.paint('dccjt1',ContextInfo.dccjt1,d,0,'noaxis')#每个周期的多头收益
	
	ContextInfo.qzzhishu.append(ContextInfo.cjt1)
	#ContextInfo.paint('qzzhishu',sum(ContextInfo.qzzhishu),d,0,'noaxis') #计算实时收益的净值
	
	ContextInfo.qzdczhishu.append(ContextInfo.dccjt1)
	#ContextInfo.paint('qzdczhishu',sum(ContextInfo.qzdczhishu),d,0,'noaxis') #计算实时对冲收益的净值
	
	for k ,closes in list(last60s.items()):
		#print k ,'股票篮子'
		if len(closes)<60:
			continue
		pre_close=closes[-1]
		m60 = np.mean(closes)
		m30 = np.mean(closes[-30:])
		m20 = np.mean(closes[-20:])
		m10 = np.mean(closes[-10:])
		m5 = np.mean(closes[-5:])
		hhv20 = max(closes[-20:])

		if pre_close >= hhv20 and pre_close > m60:               #开仓条件
			if  not (ContextInfo.HoldCircle  >= 3 and m5 < m20  and pre_close< pre_open and pre_close < m5 ): 
				if k !="000300.SH" and ContextInfo.TestHolding == 0:
					ContextInfo.holdings[k]=100
					order_shares(k,float(ContextInfo.holdings[k]), "FIX",pre_close,ContextInfo,"testS")
					ContextInfo.buypoint = closes[-1]
					#ContextInfo.HoldCircle = 1
					ContextInfo.hs300bp = ContextInfo.get_close_price("SH","000300",now,ContextInfo.perioddic[currentperiod])
					ContextInfo.hstmp = ContextInfo.hszhishu
					ContextInfo.tmp = ContextInfo.zhishu
					ContextInfo.TestHolding = 1
					ContextInfo.BuyTime = d
					#print '买入时间', millisecond2date(now)
					ContextInfo.draw_text(1,0.5,'买入')
					break

		if  ContextInfo.HoldCircle  >= 3 and m5 < m20  and pre_close< pre_open and pre_close < m5 :    #平仓条件
			if ContextInfo.TestHolding > 0:
				order_shares(k,-float(ContextInfo.holdings[k]), "FIX",pre_close,ContextInfo,"testS")
				ContextInfo.thisprofit = (closes[-1] - ContextInfo.buypoint)/ContextInfo.buypoint
				ContextInfo.HSthisprofit = (ContextInfo.get_close_price("SH","000300",now,ContextInfo.perioddic[currentperiod]) - ContextInfo.hs300bp)/ContextInfo.hs300bp
				ContextInfo.hszhishu = ContextInfo.hstmp +ContextInfo.HSthisprofit
				ContextInfo.zhishu = ContextInfo.tmp + ContextInfo.thisprofit - 0.003 
				#ContextInfo.value.append(ContextInfo.zhishu)
				ContextInfo.profit = ContextInfo.profit + ContextInfo.thisprofit
				ContextInfo.DCS += 1
				
				ContextInfo.buypoint = 0
				ContextInfo.hs300bp = 0
				ContextInfo.TestHolding = 0
				ContextInfo.BuyTime = 0
				#print '卖出时间', millisecond2date(now)
				ContextInfo.draw_text(1,0.6,'卖出')
				#ContextInfo.HoldCircle = 0
				del ContextInfo.holdings[k]
				
	#print 'ContextInfo.TestHolding',ContextInfo.TestHolding
	
	if ContextInfo.buypoint > 0:
		BYL = ContextInfo.get_close_price("SH","600000",now,ContextInfo.perioddic[currentperiod]) - ContextInfo.buypoint
	else:
		BYL = 0
	#ContextInfo.paint('BYL',BYL,-1,0,'noaxis')
	#ContextInfo.paint('vv',ContextInfo.hs300bp,-1,0,'noaxis')
	ContextInfo.paint('指数',ContextInfo.zhishu,-1,0,'noaxis')
	#ContextInfo.paint('对应指数',ContextInfo.hszhishu,-1,0,'noaxis')
	#ContextInfo.paint('对冲',ContextInfo.zhishu - ContextInfo.hszhishu,-1,0,'noaxis')
	#ContextInfo.paint('最近浮盈',ContextInfo.thisprofit,-1,0,'noaxis')
	#ContextInfo.paint('最近指数涨跌',ContextInfo.HSthisprofit,-1,0,'noaxis')
	#ContextInfo.paint('最近对冲收益', ContextInfo.thisprofit - ContextInfo.HSthisprofit,-1,0,'noaxis')
	#ContextInfo.paint('交易次数',ContextInfo.DCS,-1,0,'noaxis')
	
	ContextInfo.value.append(ContextInfo.zhishu)
	if len(ContextInfo.value):
		Recent_Drawdown = max(ContextInfo.value)-ContextInfo.zhishu
	else:
		Recent_Drawdown = 0
	#ContextInfo.paint('最近回撤',Recent_Drawdown,-1,0,'noaxis')
	ContextInfo.valuerange.append(Recent_Drawdown)
	#ContextInfo.paint('最大回撤db',max(ContextInfo.valuerange),-1,0,'noaxis')
	
	if ContextInfo.TestHolding == 1:
		ContextInfo.HoldingTime = ContextInfo.HoldingTime + 1
	#print '持仓时间',ContextInfo.HoldingTime
	#ContextInfo.paint('持仓时间',ContextInfo.HoldingTime,-1,0,'noaxis')
	if ContextInfo.get_close_price("SH","000300",now,ContextInfo.perioddic[currentperiod]) > 0:
		ContextInfo.TradeTime += 1
	#ContextInfo.paint('交易时间',ContextInfo.TradeTime,-1,0,'noaxis')
	#ContextInfo.paint('持仓',ContextInfo.TestHolding,-1,0,'noaxis')
	
	if ContextInfo.DCS > 0:
		average_unilateral = ContextInfo.zhishu/ContextInfo.DCS
		average_hegde = (ContextInfo.zhishu - ContextInfo.hszhishu)/ContextInfo.DCS
	else:
		average_unilateral = 0
		average_hegde = 0
	ContextInfo.paint('平均单边',average_unilateral,-1,0,'noaxis')
	#ContextInfo.paint('平均对冲',average_unilateral,-1,0,'noaxis')
	
	ContextInfo.hedge.append(ContextInfo.zhishu - ContextInfo.hszhishu)
	ContextInfo.hedgerange.append(max(ContextInfo.hedge)-(ContextInfo.zhishu - ContextInfo.hszhishu))
	#ContextInfo.paint('最大回撤dc',max(ContextInfo.hedgerange),-1,0,'noaxis')
	
	#ContextInfo.paint('xpdymd指数',ContextInfo.zhishu,-1,0,'noaxis')

	if ContextInfo.DCS > 0:
		win = np.array(ContextInfo.value[1:]) - np.array(ContextInfo.value[:-1])
		wintimes = float(np.sum(win>0))/ContextInfo.DCS
		#print 'np.sum(wintimes>0)',np.sum(wintimes>0),'ContextInfo.DCS',ContextInfo.DCS
	else:
		wintimes = 0
	#ContextInfo.paint('胜率',wintimes,-1,0,'noaxis')

def date2millisecond(da1):
	return int(time.mktime((int(da1[0:4]),int(da1[4:6]),int(da1[6:8]),0,0,0,0,0,0))*1000)
def millisecond2date(mdate):
	timeArray = time.localtime(mdate/1000)
	date1 = time.strftime("%Y%m%d", timeArray)
	return date1
	
def DateInterval(startdate,enddate):   #起始日期的时间间隔天数
	start = datetime.datetime(int(startdate[:4]),int(startdate[4:6]),int(startdate[6:]))
	end = datetime.datetime(int(enddate[:4]),int(enddate[4:6]),int(enddate[6:]))
	return (end - start).days



