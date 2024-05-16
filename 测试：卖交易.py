#encoding:gbk
'''
�����������趨�ý��׵Ĺ�Ʊ���ӣ�Ȼ�����ָ����CCIָ�����жϳ���ͳ���
���г���ͳ�������ʱ�����������趨�õĹ�Ʊ����
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
	���ӶϿ�
	:return:
	"""
	print("���ӶϿ�")
def on_stock_order(self, order):
	"""
	ί�лر�����
	:param order: XtOrder����
	:return:
	"""
	print("ί�лر�����:")
	print(order.stock_code, order.order_status, order.order_sysid)
	
def on_stock_asset(self, asset):
	"""
	�ʽ�䶯����
	:param asset: XtAsset����
	:return:
	"""
	print("�ʽ�䶯����")
	print(asset.account_id, asset.cash, asset.total_asset)
def on_stock_position(self, position):
	"""
	�ֱֲ䶯����
	:param position: XtPosition����
	:return:
	"""
	print("�ֱֲ䶯����")
	print(position.stock_code, position.volume)
	
def on_order_error(self, order_error):
	"""
	ί��ʧ������
	:param order_error:XtOrderError ����
	:return:
	"""
	print("ί��ʧ������")
	print(order_error.order_id, order_error.error_id, order_error.error_msg)
def on_cancel_error(self, cancel_error):
	"""
	����ʧ������
	:param cancel_error: XtCancelError ����
	:return:
	"""
	print("����ʧ������")
	print(cancel_error.order_id, cancel_error.error_id, cancel_error.error_msg)
def on_order_stock_async_response(self, response):
	"""
	�첽�µ��ر�����
	:param response: XtOrderResponse ����
	:return:
	"""
	print("�첽�µ��ر�����")
	print(response.account_id, response.order_id, response.seq)
def on_account_status(self, status):
	"""
	:param response: XtAccountStatus ����
	:return:
	"""
	print("on_account_status")
	print(status.account_id, status.account_type, status.status)
	
import time

import datetime as dt
def on_timer(ContextInfo):
	ls = globals().get("stock_list")
	now_time = dt.datetime.now().strftime("%Y%m%d %H:%M:%S")
	# ȡtick����
	ticks = ContextInfo.get_full_tick(ls)

	# �ǵ�ͳ��,��ȥ��ͣ�ƹ�
	profit_ls = [i for i in ticks if ticks[i]["lastPrice"] > ticks[i]["lastClose"] and ticks[i]["openInt"] != 1]
	loss_ls = [i for i in ticks if ticks[i]["lastPrice"] < ticks[i]["lastClose"] and ticks[i]["openInt"] != 1]
	print(f"{now_time}: �Ǽ���{len(profit_ls)}; ������{len(loss_ls)}")


c = 0
s = '000001.SZ'
def myHandlebar(C):
	global c
	now = time.strftime('%H%M%S')
	if c ==0 and '092500' >= now >= '091500':
		c += 1
		#passorder(23,1101,account,s,11,14.00,100,2,C) # �����µ�
	
def postsell(orders,deals, positions, accounts):
	# orders
	order_list = []
	for order in orders:
		o = {}
		o['m_strInstrumentID'] = order.m_strInstrumentID
		o['m_strInstrumentName'] = order.m_strInstrumentName
		o['m_nOffsetFlag'] = order.m_nOffsetFlag		# ����
		o['m_nVolumeTotalOriginal'] = order.m_nVolumeTotalOriginal		# ί������
		o['m_dTradedPrice'] = order.m_dTradedPrice		# �ɽ�����
		o['m_nVolumeTraded'] = order.m_nVolumeTraded		# �ɽ�����
		o['m_dTradeAmount'] = order.m_dTradeAmount		# �ɽ����
		#print(o)
		order_list.append(o)
	# deals
	deal_list = []
	for deal in deals:
		o = {}
		o['m_strInstrumentID'] = deal.m_strInstrumentID
		o['m_strInstrumentName'] = deal.m_strInstrumentName
		o['m_nOffsetFlag'] = deal.m_nOffsetFlag		# ����
		o['m_dPrice'] = deal.m_dPrice		# �ɽ��۸�
		o['m_nVolume'] = deal.m_nVolume		# �ɽ�����
		o['m_dTradeAmount'] = deal.m_dTradeAmount		# �ɽ����
		#print(o)
		deal_list.append(o)
	# positions
	position_list = []
	for position in positions:
		o = {}
		o['m_strInstrumentID'] = position.m_strInstrumentID
		o['m_strInstrumentName'] = position.m_strInstrumentName
		o['m_nVolume'] = position.m_nVolume		# �ֲ���
		o['m_nCanUseVolume'] = position.m_nCanUseVolume		# ��������
		o['m_dOpenPrice'] = position.m_dOpenPrice		# �ɱ���
		o['m_dInstrumentValue'] = position.m_dInstrumentValue		# ��ֵ
		o['m_dPositionCost'] = position.m_dPositionCost		# �ֲֳɱ�
		o['m_dPositionProfit'] = position.m_dPositionProfit		# ӯ��
		#print(o)
		position_list.append(o)
	# accounts
	account_list = []
	for account in accounts:
		o = {}
		o['m_dBalance'] = account.m_dBalance		# ���ʲ�
		o['m_dAssureAsset'] = account.m_dAssureAsset		# ���ʲ�
		o['m_dInstrumentValue'] = account.m_dInstrumentValue		# ����ֵ
		o['m_dAvailable'] = account.m_dAvailable		# ���ý��
		o['m_dPositionProfit'] = account.m_dPositionProfit		# ӯ��
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
	print("sell��һЩ")

# ��λ
cw = 0.9
# �ֹ�����
zdcg = 1

def init(C):
	'''
	First:
		Gain the account fund
	'''
	C.run_time("myHandlebar","5nSecond","2019-10-14 13:20:00")
	orders, deals, positions, accounts = query_info(C)					# ��ѯ�˻���Ϣ
	A.waiting_list = [] #δ�鵽ί���б� ����δ�鵽ί�������ͣ�������� ��ֹ����
	A.buy_code = 23  #�������� ���ֹ�Ʊ �� �����˺�
	A.sell_code = 24
	# orders:
	#print(f'{accountObj["position"]["m_strInstrumentName"]}:{accountObj["position"]["m_nVolume"]}')
	#globals()["stock_list"] = get_stock_list_in_sector("���A��")
	# ��2023-12-31 23:59:59��ÿ60s����һ��on_timer
	#tid=ContextInfo.schedule_run(on_timer,'20231231235959',3,dt.timedelta(seconds=60),'my_timer')
	# ȡ��������Ϊ"my_timer"������
	# # ContextInfo.cancel_schedule_run('my_timer')

def handlebar(C):
	# if not C.is_last_bar():
	# 	return
		# orders:list ��Ʊ����m_strInstrumentID,����:m_strInstrumentName,��������m_nOffsetFlag,ί������m_nVolumeTotalOriginal,�ɽ�����m_dTradedPrice,�ɽ�����m_nVolumeTraded
	orders, deals, positions, accounts = query_info(C)		# ��ѯ�˻���Ϣ
	
	accountObj['all_bullet'] = accounts[0].m_dBalance		# �������
	accountObj['bullet'] = accounts[0].m_dAvailable			# �������
	accountObj['max_use_bullet'] = accounts[0].m_dBalance * max_rate
	
	# ���㱱��������
	north_finance_info = C.get_north_finance_change('1m')
	north_finance_info_value = C.get_north_finance_change('1m')[list(C.get_north_finance_change('1m').keys())[0]]
	all_buy = float(north_finance_info_value['hgtNorthBuyMoney'] + north_finance_info_value['hgtSouthBuyMoney'] + north_finance_info_value['sgtNorthBuyMoney'] + north_finance_info_value['sgtSouthBuyMoney'])/100000000
	all_sell = float(north_finance_info_value['hgtNorthSellMoney'] + north_finance_info_value['hgtSouthSellMoney'] + north_finance_info_value['sgtNorthSellMoney'] + north_finance_info_value['sgtSouthSellMoney'])/100000000
	print(f'������:{all_buy}��-----������:{all_sell}')
	# ������̳ɽ���
	A_all=0
	for code in ['000001.SH', '399001.SZ']:
		tick = C.get_full_tick([code])
		A_all = A_all + tick[code]['amount']
	print(f'�ɽ���:{A_all/100000000}')
	if accountObj["financial_status"] != 0:
		print(f'���̱䶯��{A_all/100000000 - accountObj["financial_status"]:.2f}��,�ٷֱ�:{(A_all/100000000)/(accountObj["financial_status"])/100:.2f}%')
	accountObj['financial_status'] = A_all/100000000
	#------------------
	# �Ƿ񳷵�
	#if A.waiting_list:
	#	found_list = []
	#	orders = get_trade_detail_data(A.acct, A.acct_type, 'order')
	#	for order in orders:
	#		if order.m_strRemark in A.waiting_list:
	#			found_list.append(order.m_strRemark)
	#	A.waiting_list = [i for i in A.waiting_list if i not in found_list]
	#if A.waiting_list:
	#	print(f"��ǰ��δ�鵽ί�� {A.waiting_list} ��ͣ��������")
	#	return
	# ��
	if positions[0].m_nVolume == 0 and positions[0].m_nCanUseVolume == 0 :
		if 1 - (accountObj['bullet'] / accountObj['all_bullet']) <= cw:
			res = do_buy()
			res_code_list = json.loads(res.text)		# �������list
			tick = C.get_full_tick(res_code_list)
			sell_1 = tick[res_code_list[0]]['askPrice'][0]
			if tick[res_code_list[0]]['askPrice'][0]*100 !=0:
				buy_hand_num = accountObj['bullet'] / (tick[res_code_list[0]]['askPrice'][0]*100)
				sell_hand = tick[res_code_list[0]]['askVol'][0]
				if sell_hand> buy_hand_num:
					# ��14.00Ԫ�޼������Ʊs 100��
					passorder(23,1101,account, res_code_list[0],11,sell_1,int(buy_hand_num)*100,1,C)  # ��ǰk��Ϊ����k�� �������µ�
					# if False:
					# 	for o in orders:
					# 		cancel(o.m_strOrderSysID, account,'stock',C)
	# ��
	else:
		# �Ⱦ���Ҫ��Ҫ�����ٷ���ʲô�ʺ��������
		# �ֲ�code
		#if accountObj['positions']['m_nCanUseVolume'] > 0:		# �Ƿ��п���������Ʊ
		if positions[0].m_nCanUseVolume > 0:		# �Ƿ��п���������Ʊ
			result = postsell(orders, deals, positions, accounts)
			if json.loads(result.text)["result"] == "True":
			#if json.loads(result.text)["result"] == "False":
			# SELL----------------------------------------------------------------------------------------------------------------------------------
			#if sum(tick[code]['askVol']) * 100 >= accountObj['positions']['m_nVolume']:
				#accountObj['positions']['m_nVolume'] #�ֹ����� p
				#print(f"����:{accountObj['positions']['m_nVolume']}")
				#print(tick)
				#passorder(24, 1101, account, code, 5, -1, accountObj['positions']['m_nVolume'], C)  # 23�� # 24��
				#for code in ['000001.SH', '399001.SZ']:
				#	passorder(23, 1101, account, code, 5, -1, accountObj['max_use_bullet'], C)  # 23�� # 24��
				#	tick = C.get_full_tick([code])
				#	print(tick[code])
				#	print(f'����:{code},����:{accountObj["max_use_bullet"]}')
				stock_list = [holding.m_strInstrumentID + '.' + holding.m_strExchangeID for holding in positions]
				if stock_list:					# ����п�������Ʊ ��ִ��
					full_tick = C.get_full_tick(stock_list)				# ��ù�Ʊÿ��timetage ����Ϣ
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
							stop_price = round(stop_price, 2)			# ��ͣ��
							ask_price_3 = full_tick[stock]['bidPrice'][2]
							if not ask_price_3:
								print(f"{stock} {full_tick[stock]} δȡ�������̿ڼ� ����ͻ������½� ������� �Ƿ�ѡ�����嵵���� ������������")
								continue
							if high_price == stop_price and current_price < stop_price:
								msg = f"{stock} ��ͣ�� ���� ���� {volume}��"
								print(msg)
								passorder(24, 1101, account, stock, 14, -1, volume, '��ͣ����', 2, msg, C)
								continue
							code = gp_type_szsh(accountObj["positions"]['m_strInstrumentID'])
							# �ֲ�code info
							tick = C.get_full_tick([code])
							if tick[code]["bidPrice"][0] != 0:
								print(f'�ɱ���:{accountObj["positions"]["m_dOpenPrice"]:.2f}-----���:{accountObj["positions"]["m_dOpenPrice"] / tick[code]["bidPrice"][0]:.2f}% ---- ӯ��:{accounts[0].m_dPositionProfit:.2f}')
								print(f'��:{tick[code]["askPrice"]}----{tick[code]["askVol"]}---- ��:{sum(tick[code]["askVol"])} ----���:{[str(tick[code]["askPrice"][i] * tick[code]["askVol"][i] * 100 / 10000) + "��" for i in range(len(tick[code]["askPrice"]))]}----��:{sum([tick[code]["askPrice"][i] * tick[code]["askVol"][i] * 100 / 10000 for i in range(len(tick[code]["askPrice"]))]):.2f}��')
								print(f'��:{tick[code]["bidPrice"]}----{tick[code]["bidVol"]}---- ��:{sum(tick[code]["bidVol"])} ----���:{[str(tick[code]["bidPrice"][i] * tick[code]["bidVol"][i] * 100 /10000) + "��" for i in range(len(tick[code]["bidPrice"]))]}----��:{sum([tick[code]["bidPrice"][i] * tick[code]["bidVol"][i] * 100 /10000 for i in range(len(tick[code]["bidPrice"]))]):.2f}��')
							if accountObj['amount']!=0:
								print(f'���ɳɽ�����{(tick[code]["amount"] - accountObj["amount"])/100}�� ---- ���ɳɽ��{(tick[code]["amount"] - accountObj["amount"]) * tick[code]["bidPrice"][0] / 10000:.4f} ��')
								if (tick[code]["amount"] - accountObj["amount"])/100 > 6000 :
									#or (tick[code]["amount"] - (tick[code]["amount"] - accountObj["amount"]) * tick[code]["bidPrice"][0] / 10000) > 600
									print("�������ָ磡���������������������ָ��𣡣���������������������������������������������������������������������������������������������")
								elif (tick[code]["amount"] - accountObj["amount"])/100 > 3000:
									print("����ǧ�ֹ���~~~  ��ʼ����--------------------------~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
								if sum(tick[code]["askVol"]) * 4 < sum(tick[code]["bidVol"]):
									print("�շ������������-----------------------�ɼۿ���������")
								elif sum(tick[code]["bidVol"]) * 4 < sum(tick[code]["askVol"]):
									print("�нӷ������������------------------��������------------�����Ƕ��ڸߵ�")
								
							msg = f'{stock} ӯ������ {rate} ����-10% ���� {volume}��'
							print(msg)
							passorder(24, 1101, account, stock, 14, -1, volume, '����ģ��', 2, msg, C)
								
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
	# # ʹ��smart_algo_passorder �µ�
	#print("ʹ��smart_algo_passorder �µ�")
	pass

def query_info(C):
	"""
	�û�����
	"""
	account = '8881667160'
	orders = get_trade_detail_data(account, 'stock', 'order')
	#for o in orders:
	#	print(f'��Ʊ����: {o.m_strInstrumentID}, �г�����: {o.m_strExchangeID}, ֤ȯ����: {o.m_strInstrumentName}, ��������: {o.m_nOffsetFlag}',
	#	f'ί������: {o.m_nVolumeTotalOriginal}, �ɽ�����: {o.m_dTradedPrice}, �ɽ�����: {o.m_nVolumeTraded}, �ɽ����:{o.m_dTradeAmount}')

	deals = get_trade_detail_data(account , 'stock', 'deal')
	#for dt in deals:
	#	print(f'��Ʊ����: {dt.m_strInstrumentID}, �г�����: {dt.m_strExchangeID}, ֤ȯ����: {dt.m_strInstrumentName}, ��������: {dt.m_nOffsetFlag}', 
	#	f'�ɽ��۸�: {dt.m_dPrice}, �ɽ�����: {dt.m_nVolume}, �ɽ����: {dt.m_dTradeAmount}')

	positions = get_trade_detail_data(account, 'stock', 'position')
	#for dt in positions:
	#	print(f'��Ʊ����: {dt.m_strInstrumentID}, �г�����: {dt.m_strExchangeID}, ֤ȯ����: {dt.m_strInstrumentName}, �ֲ���: {dt.m_nVolume}, ��������: {dt.m_nCanUseVolume}',
	#	f'�ɱ���: {dt.m_dOpenPrice:.2f}, ��ֵ: {dt.m_dInstrumentValue:.2f}, �ֲֳɱ�: {dt.m_dPositionCost:.2f}, ӯ��: {dt.m_dPositionProfit:.2f}')

	accounts = get_trade_detail_data(account , 'stock', 'account')
	#for dt in accounts:
	#	print(f'���ʲ�: {dt.m_dBalance:.2f}, ���ʲ�: {dt.m_dAssureAsset:.2f}, ����ֵ: {dt.m_dInstrumentValue:.2f}', 
	#	f'�ܸ�ծ: {dt.m_dTotalDebit:.2f}, ���ý��: {dt.m_dAvailable:.2f}, ӯ��: {dt.m_dPositionProfit:.2f}',
	#	f'')
	
	# orders:
	for order in orders:
		o = {}
		o['m_strInstrumentID'] = order.m_strInstrumentID
		o['m_strInstrumentName'] = order.m_strInstrumentName
		o['m_nOffsetFlag'] = order.m_nOffsetFlag						# ����
		o['m_nVolumeTotalOriginal'] = order.m_nVolumeTotalOriginal		# ί������
		o['m_dTradedPrice'] = order.m_dTradedPrice					# �ɽ�����
		o['m_nVolumeTraded'] = order.m_nVolumeTraded				# �ɽ�����
		o['m_dTradeAmount'] = order.m_dTradeAmount					# �ɽ����
		accountObj["orders"] = o
	# deals:
	for deal in deals:
		o = {}
		o['m_strInstrumentID'] = deal.m_strInstrumentID
		o['m_strInstrumentName'] = deal.m_strInstrumentName
		o['m_nOffsetFlag'] = deal.m_nOffsetFlag						# ����
		o['m_dPrice'] = deal.m_dPrice								# �ɽ��۸�
		o['m_nVolume'] = deal.m_nVolume								# �ɽ�����
		o['m_dTradeAmount'] = deal.m_dTradeAmount					# �ɽ����
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
		o['m_nVolume'] = position.m_nVolume							# �ֲ���
		o['m_nCanUseVolume'] = position.m_nCanUseVolume				# ��������
		o['m_dOpenPrice'] = position.m_dOpenPrice					# �ɱ���
		o['m_dInstrumentValue'] = position.m_dInstrumentValue		# ��ֵ
		o['m_dPositionCost'] = position.m_dPositionCost				# �ֲֳɱ�
		o['m_dPositionProfit'] = position.m_dPositionProfit			# ӯ��
		accountObj["positions"] = o
	
	# accounts:
	for account in accounts:
		o = {}
		o['m_dBalance'] = account.m_dBalance		# ���ʲ�
		o['m_dAssureAsset'] = account.m_dAssureAsset		# ���ʲ�
		o['m_dInstrumentValue'] = account.m_dInstrumentValue		# ����ֵ
		o['m_dAvailable'] = account.m_dAvailable		# ���ý��
		o['m_dPositionProfit'] = account.m_dPositionProfit		# ӯ��
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
	print('�ʽ��˺�״̬�仯����:')
	print(show_data(accountInfo)) 


