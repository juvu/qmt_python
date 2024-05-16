#encoding:gbk
'''
本策略事先设定好交易的股票篮子，然后根据指数的CCI指标来判断超买和超卖
当有超买和超卖发生时，交易事先设定好的股票篮子
'''
import pandas as pd
import numpy as np
import talib
import requests
import json
from xtquant import xtdata

account = '8881667160'
max_rate = 0.5
url = "http://127.0.0.1:8000"

accountObj={'code_list':('002933.SZ'),		#
			'trading_snapshot':[],			#
			'orders':{},					# 
			'deals':{},					# 
			'positions':{},					# 
			'accounts':{},					# 
			'financial_status':0.0,
			'amount':0,
	}

def gp_type_szsh(code):
	if code.find('60',0,3)==0:
		code=code + '.SH'
	elif code.find('688',0,4)==0:
		code=code + '.SH'
	elif code.find('900',0,4)==0:
		code=code + '.SH'
	elif code.find('00',0,3)==0:
		code=code + '.SZ'
	elif code.find('300',0,4)==0:
		code=code + '.SZ'
	elif code.find('200',0,4)==0:
		code=code + '.SZ'
	return code


class a():
	pass
A = a()
def on_data(datas):
	for stock_code in datas:
		print(stock_code, datas[stock_code])
def on_disconnected(self):
	"""
	连接断开
	:return:
	"""
	print("连接断开")
def on_stock_order(self, order):
	"""
	委托回报推送
	:param order: XtOrder对象
	:return:
	"""
	print("委托回报推送:")
	print(order.stock_code, order.order_status, order.order_sysid)
	
def on_stock_asset(self, asset):
	"""
	资金变动推送
	:param asset: XtAsset对象
	:return:
	"""
	print("资金变动推送")
	print(asset.account_id, asset.cash, asset.total_asset)
def on_stock_position(self, position):
	"""
	持仓变动推送
	:param position: XtPosition对象
	:return:
	"""
	print("持仓变动推送")
	print(position.stock_code, position.volume)
	
def on_order_error(self, order_error):
	"""
	委托失败推送
	:param order_error:XtOrderError 对象
	:return:
	"""
	print("委托失败推送")
	print(order_error.order_id, order_error.error_id, order_error.error_msg)
def on_cancel_error(self, cancel_error):
	"""
	撤单失败推送
	:param cancel_error: XtCancelError 对象
	:return:
	"""
	print("撤单失败推送")
	print(cancel_error.order_id, cancel_error.error_id, cancel_error.error_msg)
def on_order_stock_async_response(self, response):
	"""
	异步下单回报推送
	:param response: XtOrderResponse 对象
	:return:
	"""
	print("异步下单回报推送")
	print(response.account_id, response.order_id, response.seq)
def on_account_status(self, status):
	"""
	:param response: XtAccountStatus 对象
	:return:
	"""
	print("on_account_status")
	print(status.account_id, status.account_type, status.status)
	
import time

import datetime as dt
def on_timer(ContextInfo):
	ls = globals().get("stock_list")
	now_time = dt.datetime.now().strftime("%Y%m%d %H:%M:%S")
	# 取tick数据
	ticks = ContextInfo.get_full_tick(ls)

	# 涨跌统计,并去除停牌股
	profit_ls = [i for i in ticks if ticks[i]["lastPrice"] > ticks[i]["lastClose"] and ticks[i]["openInt"] != 1]
	loss_ls = [i for i in ticks if ticks[i]["lastPrice"] < ticks[i]["lastClose"] and ticks[i]["openInt"] != 1]
	print(f"{now_time}: 涨家数{len(profit_ls)}; 跌家数{len(loss_ls)}")


c = 0
s = '000001.SZ'
def myHandlebar(C):
	global c
	now = time.strftime('%H%M%S')
	if c ==0 and '092500' >= now >= '091500':
		c += 1
		#passorder(23,1101,account,s,11,14.00,100,2,C) # 立即下单
	
def postsell(orders,deals, positions, accounts):
	# orders
	order_list = []
	for order in orders:
		o = {}
		o['m_strInstrumentID'] = order.m_strInstrumentID
		o['m_strInstrumentName'] = order.m_strInstrumentName
		o['m_nOffsetFlag'] = order.m_nOffsetFlag		# 卖卖
		o['m_nVolumeTotalOriginal'] = order.m_nVolumeTotalOriginal		# 委托数量
		o['m_dTradedPrice'] = order.m_dTradedPrice		# 成交均价
		o['m_nVolumeTraded'] = order.m_nVolumeTraded		# 成交数量
		o['m_dTradeAmount'] = order.m_dTradeAmount		# 成交金额
		#print(o)
		order_list.append(o)
	# deals
	deal_list = []
	for deal in deals:
		o = {}
		o['m_strInstrumentID'] = deal.m_strInstrumentID
		o['m_strInstrumentName'] = deal.m_strInstrumentName
		o['m_nOffsetFlag'] = deal.m_nOffsetFlag		# 卖卖
		o['m_dPrice'] = deal.m_dPrice		# 成交价格
		o['m_nVolume'] = deal.m_nVolume		# 成交数量
		o['m_dTradeAmount'] = deal.m_dTradeAmount		# 成交金额
		#print(o)
		deal_list.append(o)
	# positions
	position_list = []
	for position in positions:
		o = {}
		o['m_strInstrumentID'] = position.m_strInstrumentID
		o['m_strInstrumentName'] = position.m_strInstrumentName
		o['m_nVolume'] = position.m_nVolume		# 持仓量
		o['m_nCanUseVolume'] = position.m_nCanUseVolume		# 可用数量
		o['m_dOpenPrice'] = position.m_dOpenPrice		# 成本价
		o['m_dInstrumentValue'] = position.m_dInstrumentValue		# 市值
		o['m_dPositionCost'] = position.m_dPositionCost		# 持仓成本
		o['m_dPositionProfit'] = position.m_dPositionProfit		# 盈亏
		#print(o)
		position_list.append(o)
	# accounts
	account_list = []
	for account in accounts:
		o = {}
		o['m_dBalance'] = account.m_dBalance		# 总资产
		o['m_dAssureAsset'] = account.m_dAssureAsset		# 净资产
		o['m_dInstrumentValue'] = account.m_dInstrumentValue		# 总市值
		o['m_dAvailable'] = account.m_dAvailable		# 可用金额
		o['m_dPositionProfit'] = account.m_dPositionProfit		# 盈亏
		#print(o)
		account_list.append(o)
	demo_url = url+'/sell'
	res = requests.post(demo_url,data = json.dumps({"orders":order_list,'deals':deal_list,"positions":position_list,"accounts":account_list}))
	return res
	
def getbuy_codes():
	demo_url = url+'/buy'
	res = requests.get(demo_url)
	return res
	
def do_buy():
	demo_url = url+'/buy'
	res = requests.get(demo_url,params={'zdcg':zdcg})
	return res
	

def do_sell():
	print("sell了一些")

# 仓位
cw = 0.9
# 持股数量
zdcg = 1

def init(C):
	'''
	First:
		Gain the account fund
	'''
	C.run_time("myHandlebar","5nSecond","2019-10-14 13:20:00")
	orders, deals, positions, accounts = query_info(C)					# 查询账户信息
	A.waiting_list = [] #未查到委托列表 存在未查到委托情况暂停后续报单 防止超单
	A.buy_code = 23  #买卖代码 区分股票 与 两融账号
	A.sell_code = 24
	# orders:
	#print(f'{accountObj["position"]["m_strInstrumentName"]}:{accountObj["position"]["m_nVolume"]}')
	#globals()["stock_list"] = get_stock_list_in_sector("沪深京A股")
	# 自2023-12-31 23:59:59后每60s运行一次on_timer
	#tid=ContextInfo.schedule_run(on_timer,'20231231235959',3,dt.timedelta(seconds=60),'my_timer')
	# 取消任务组为"my_timer"的任务
	# # ContextInfo.cancel_schedule_run('my_timer')

def handlebar(C):
	# if not C.is_last_bar():
	# 	return
		# orders:list 股票代码m_strInstrumentID,名称:m_strInstrumentName,买卖方向m_nOffsetFlag,委托数量m_nVolumeTotalOriginal,成交均价m_dTradedPrice,成交数量m_nVolumeTraded
	orders, deals, positions, accounts = query_info(C)		# 查询账户信息
	
	accountObj['all_bullet'] = accounts[0].m_dBalance		# 所有余额
	accountObj['bullet'] = accounts[0].m_dAvailable			# 可用余额
	accountObj['max_use_bullet'] = accounts[0].m_dBalance * max_rate
	
	# 计算北向总买卖
	north_finance_info = C.get_north_finance_change('1m')
	north_finance_info_value = C.get_north_finance_change('1m')[list(C.get_north_finance_change('1m').keys())[0]]
	all_buy = float(north_finance_info_value['hgtNorthBuyMoney'] + north_finance_info_value['hgtSouthBuyMoney'] + north_finance_info_value['sgtNorthBuyMoney'] + north_finance_info_value['sgtSouthBuyMoney'])/100000000
	all_sell = float(north_finance_info_value['hgtNorthSellMoney'] + north_finance_info_value['hgtSouthSellMoney'] + north_finance_info_value['sgtNorthSellMoney'] + north_finance_info_value['sgtSouthSellMoney'])/100000000
	print(f'总买入:{all_buy}亿-----总卖出:{all_sell}')
	# 计算大盘成交额
	A_all=0
	for code in ['000001.SH', '399001.SZ']:
		tick = C.get_full_tick([code])
		A_all = A_all + tick[code]['amount']
	print(f'成交额:{A_all/100000000}')
	if accountObj["financial_status"] != 0:
		print(f'大盘变动：{A_all/100000000 - accountObj["financial_status"]:.2f}亿,百分比:{(A_all/100000000)/(accountObj["financial_status"])/100:.2f}%')
	accountObj['financial_status'] = A_all/100000000
	#------------------
	# 是否撤单
	#if A.waiting_list:
	#	found_list = []
	#	orders = get_trade_detail_data(A.acct, A.acct_type, 'order')
	#	for order in orders:
	#		if order.m_strRemark in A.waiting_list:
	#			found_list.append(order.m_strRemark)
	#	A.waiting_list = [i for i in A.waiting_list if i not in found_list]
	#if A.waiting_list:
	#	print(f"当前有未查到委托 {A.waiting_list} 暂停后续报单")
	#	return
	# 买
	if positions[0].m_nVolume == 0 and positions[0].m_nCanUseVolume == 0 :
		if 1 - (accountObj['bullet'] / accountObj['all_bullet']) <= cw:
			res = do_buy()
			res_code_list = json.loads(res.text)		# 待购买的list
			tick = C.get_full_tick(res_code_list)
			sell_1 = tick[res_code_list[0]]['askPrice'][0]
			if tick[res_code_list[0]]['askPrice'][0]*100 !=0:
				buy_hand_num = accountObj['bullet'] / (tick[res_code_list[0]]['askPrice'][0]*100)
				sell_hand = tick[res_code_list[0]]['askVol'][0]
				if sell_hand> buy_hand_num:
					# 用14.00元限价买入股票s 100股
					passorder(23,1101,account, res_code_list[0],11,sell_1,int(buy_hand_num)*100,1,C)  # 当前k线为最新k线 则立即下单
					# if False:
					# 	for o in orders:
					# 		cancel(o.m_strOrderSysID, account,'stock',C)
	# 卖
	else:
		# 先决定要不要卖，再分析什么适合卖最合适
		# 持仓code
		#if accountObj['positions']['m_nCanUseVolume'] > 0:		# 是否有可以卖出的票
		if positions[0].m_nCanUseVolume > 0:		# 是否有可以卖出的票
			result = postsell(orders, deals, positions, accounts)
			if json.loads(result.text)["result"] == "True":
			#if json.loads(result.text)["result"] == "False":
			# SELL----------------------------------------------------------------------------------------------------------------------------------
			#if sum(tick[code]['askVol']) * 100 >= accountObj['positions']['m_nVolume']:
				#accountObj['positions']['m_nVolume'] #持股数量 p
				#print(f"卖出:{accountObj['positions']['m_nVolume']}")
				#print(tick)
				#passorder(24, 1101, account, code, 5, -1, accountObj['positions']['m_nVolume'], C)  # 23买 # 24卖
				#for code in ['000001.SH', '399001.SZ']:
				#	passorder(23, 1101, account, code, 5, -1, accountObj['max_use_bullet'], C)  # 23买 # 24卖
				#	tick = C.get_full_tick([code])
				#	print(tick[code])
				#	print(f'买入:{code},数量:{accountObj["max_use_bullet"]}')
				stock_list = [holding.m_strInstrumentID + '.' + holding.m_strExchangeID for holding in positions]
				if stock_list:					# 如果有可以卖的票 则执行
					full_tick = C.get_full_tick(stock_list)				# 获得股票每个timetage 的信息
					for holding in positions:
						stock = holding.m_strInstrumentID + '.' + holding.m_strExchangeID
						rate = holding.m_dProfitRate
						volume = holding.m_nCanUseVolume
						if volume < 100:
							continue
						#if stock in C.spare_list:
						#	continue
						if stock in full_tick:
							current_price = full_tick[stock]['lastPrice']
							pre_price = full_tick[stock]['lastClose']
							high_price = full_tick[stock]['high']
							stop_price = pre_price * 1.2 if stock[:2] in ['30', '68'] else pre_price * 1.1
							stop_price = round(stop_price, 2)			# 涨停价
							ask_price_3 = full_tick[stock]['bidPrice'][2]
							if not ask_price_3:
								print(f"{stock} {full_tick[stock]} 未取到三档盘口价 请检查客户端右下角 行情界面 是否选择了五档行情 本次跳过卖出")
								continue
							if high_price == stop_price and current_price < stop_price:
								msg = f"{stock} 涨停后 开板 卖出 {volume}股"
								print(msg)
								passorder(24, 1101, account, stock, 14, -1, volume, '涨停减仓', 2, msg, C)
								continue
							code = gp_type_szsh(accountObj["positions"]['m_strInstrumentID'])
							# 持仓code info
							tick = C.get_full_tick([code])
							if tick[code]["bidPrice"][0] != 0:
								print(f'成本价:{accountObj["positions"]["m_dOpenPrice"]:.2f}-----振幅:{accountObj["positions"]["m_dOpenPrice"] / tick[code]["bidPrice"][0]:.2f}% ---- 盈亏:{accounts[0].m_dPositionProfit:.2f}')
								print(f'卖:{tick[code]["askPrice"]}----{tick[code]["askVol"]}---- 手:{sum(tick[code]["askVol"])} ----金额:{[str(tick[code]["askPrice"][i] * tick[code]["askVol"][i] * 100 / 10000) + "万" for i in range(len(tick[code]["askPrice"]))]}----总:{sum([tick[code]["askPrice"][i] * tick[code]["askVol"][i] * 100 / 10000 for i in range(len(tick[code]["askPrice"]))]):.2f}万')
								print(f'买:{tick[code]["bidPrice"]}----{tick[code]["bidVol"]}---- 手:{sum(tick[code]["bidVol"])} ----金额:{[str(tick[code]["bidPrice"][i] * tick[code]["bidVol"][i] * 100 /10000) + "万" for i in range(len(tick[code]["bidPrice"]))]}----总:{sum([tick[code]["bidPrice"][i] * tick[code]["bidVol"][i] * 100 /10000 for i in range(len(tick[code]["bidPrice"]))]):.2f}万')
							if accountObj['amount']!=0:
								print(f'个股成交量：{(tick[code]["amount"] - accountObj["amount"])/100}手 ---- 个股成交额：{(tick[code]["amount"] - accountObj["amount"]) * tick[code]["bidPrice"][0] / 10000:.4f} 万')
								if (tick[code]["amount"] - accountObj["amount"])/100 > 6000 :
									#or (tick[code]["amount"] - (tick[code]["amount"] - accountObj["amount"]) * tick[code]["bidPrice"][0] / 10000) > 600
									print("出现万手哥！！！！！！！！！！万手哥点火！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！")
								elif (tick[code]["amount"] - accountObj["amount"])/100 > 3000:
									print("出现千手观音~~~  开始波动--------------------------~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
								if sum(tick[code]["askVol"]) * 4 < sum(tick[code]["bidVol"]):
									print("空方力量大幅减少-----------------------股价可能往上走")
								elif sum(tick[code]["bidVol"]) * 4 < sum(tick[code]["askVol"]):
									print("承接方力量大幅减少------------------谨慎下砸------------可能是短期高点")
								
							msg = f'{stock} 盈亏比例 {rate} 大于-10% 卖出 {volume}股'
							print(msg)
							passorder(24, 1101, account, stock, 14, -1, volume, '减仓模型', 2, msg, C)
								
							#accountObj["amount"] = tick[code]["amount"]
							#sell_ask = 0
							#buy_ask = 0
							#for i in tick[code]["askPrice"]:
							#	sell_ask = sell_ask + i
							#	
							#for i in tick[code]["bidPrice"]:
							#	buy_ask = buy_ask + i
		#print(f"sell_ask:{sell_ask:.4f}")
		#print(f"buy_ask:{buy_ask:.4f}")
		
		
	#print(dir(orders[0]))
	
def after_init(C):
	# # 使用smart_algo_passorder 下单
	#print("使用smart_algo_passorder 下单")
	pass

def query_info(C):
	"""
	用户管理
	"""
	account = '8881667160'
	orders = get_trade_detail_data(account, 'stock', 'order')
	#for o in orders:
	#	print(f'股票代码: {o.m_strInstrumentID}, 市场类型: {o.m_strExchangeID}, 证券名称: {o.m_strInstrumentName}, 买卖方向: {o.m_nOffsetFlag}',
	#	f'委托数量: {o.m_nVolumeTotalOriginal}, 成交均价: {o.m_dTradedPrice}, 成交数量: {o.m_nVolumeTraded}, 成交金额:{o.m_dTradeAmount}')

	deals = get_trade_detail_data(account , 'stock', 'deal')
	#for dt in deals:
	#	print(f'股票代码: {dt.m_strInstrumentID}, 市场类型: {dt.m_strExchangeID}, 证券名称: {dt.m_strInstrumentName}, 买卖方向: {dt.m_nOffsetFlag}', 
	#	f'成交价格: {dt.m_dPrice}, 成交数量: {dt.m_nVolume}, 成交金额: {dt.m_dTradeAmount}')

	positions = get_trade_detail_data(account, 'stock', 'position')
	#for dt in positions:
	#	print(f'股票代码: {dt.m_strInstrumentID}, 市场类型: {dt.m_strExchangeID}, 证券名称: {dt.m_strInstrumentName}, 持仓量: {dt.m_nVolume}, 可用数量: {dt.m_nCanUseVolume}',
	#	f'成本价: {dt.m_dOpenPrice:.2f}, 市值: {dt.m_dInstrumentValue:.2f}, 持仓成本: {dt.m_dPositionCost:.2f}, 盈亏: {dt.m_dPositionProfit:.2f}')

	accounts = get_trade_detail_data(account , 'stock', 'account')
	#for dt in accounts:
	#	print(f'总资产: {dt.m_dBalance:.2f}, 净资产: {dt.m_dAssureAsset:.2f}, 总市值: {dt.m_dInstrumentValue:.2f}', 
	#	f'总负债: {dt.m_dTotalDebit:.2f}, 可用金额: {dt.m_dAvailable:.2f}, 盈亏: {dt.m_dPositionProfit:.2f}',
	#	f'')
	
	# orders:
	for order in orders:
		o = {}
		o['m_strInstrumentID'] = order.m_strInstrumentID
		o['m_strInstrumentName'] = order.m_strInstrumentName
		o['m_nOffsetFlag'] = order.m_nOffsetFlag						# 卖卖
		o['m_nVolumeTotalOriginal'] = order.m_nVolumeTotalOriginal		# 委托数量
		o['m_dTradedPrice'] = order.m_dTradedPrice					# 成交均价
		o['m_nVolumeTraded'] = order.m_nVolumeTraded				# 成交数量
		o['m_dTradeAmount'] = order.m_dTradeAmount					# 成交金额
		accountObj["orders"] = o
	# deals:
	for deal in deals:
		o = {}
		o['m_strInstrumentID'] = deal.m_strInstrumentID
		o['m_strInstrumentName'] = deal.m_strInstrumentName
		o['m_nOffsetFlag'] = deal.m_nOffsetFlag						# 卖卖
		o['m_dPrice'] = deal.m_dPrice								# 成交价格
		o['m_nVolume'] = deal.m_nVolume								# 成交数量
		o['m_dTradeAmount'] = deal.m_dTradeAmount					# 成交金额
		if deal.m_nOffsetFlag==48:
			accountObj['code_list'] = [gp_type_szsh(deal.m_strInstrumentID)]
			#accountObj['code_list'].__add__(deal.m_strInstrumentID)
		else:
			accountObj['code_list'] =tuple(list(accountObj['code_list']).remove(deal.m_strInstrumentID)) if deal.m_strInstrumentID in list(accountObj['code_list']) else accountObj['code_list']
		accountObj["deals"] = o
	# positions:
	for position in positions:
		o = {}
		o['m_strInstrumentID'] = position.m_strInstrumentID
		o['m_strInstrumentName'] = position.m_strInstrumentName
		o['m_nVolume'] = position.m_nVolume							# 持仓量
		o['m_nCanUseVolume'] = position.m_nCanUseVolume				# 可用数量
		o['m_dOpenPrice'] = position.m_dOpenPrice					# 成本价
		o['m_dInstrumentValue'] = position.m_dInstrumentValue		# 市值
		o['m_dPositionCost'] = position.m_dPositionCost				# 持仓成本
		o['m_dPositionProfit'] = position.m_dPositionProfit			# 盈亏
		accountObj["positions"] = o
	
	# accounts:
	for account in accounts:
		o = {}
		o['m_dBalance'] = account.m_dBalance		# 总资产
		o['m_dAssureAsset'] = account.m_dAssureAsset		# 净资产
		o['m_dInstrumentValue'] = account.m_dInstrumentValue		# 总市值
		o['m_dAvailable'] = account.m_dAvailable		# 可用金额
		o['m_dPositionProfit'] = account.m_dPositionProfit		# 盈亏
		accountObj["accounts"] = o
	
	return orders, deals, positions, accounts
	

def show_data(data):
	tdata = {}
	for ar in dir(data):
		if ar[:2] != 'm_':continue
		# try:
		# 	tdata[ar] = data.__getattribute__(ar)
		# except:
		# 	tdata[ar] = '<CanNotConvert>'
	return tdata
	
def account_callback(ContextInfo, accountInfo):
	print('资金账号状态变化主推:')
	print(show_data(accountInfo)) 


