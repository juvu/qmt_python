# encoding:gbk
'''
本策略事先设定好交易的股票篮子，然后根据指数的CCI指标来判断超买和超卖
当有超买和超卖发生时，交易事先设定好的股票篮子
'''
import pandas as pd
import numpy as np
import talib
import socket
import sys
import threading
import queue
import time
import requests
import json
import psycopg2

print(sys.version)
print('编译器位置：' + sys.executable)


def receive_data(sock, message_queue):
    while True:
        data = sock.recv(1024)
        if not data:
            break
        print(data.decode('gbk'))
        message_queue.put(data)


def send_data(sock, message):
    sock.sendall(message.encode('utf-8'))


server_host = '127.0.0.1'
server_port = 8083
# 创建socket对象
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
message_queue = queue.Queue()
a = 0

conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="wcsql",
    user="postgres",
    password="123456"
)


def init(ContextInfo):
    # ContextInfo.run_time("myHandlebar","5nSecond","2024-01-10 13:20:00")
    print("当前周期是:" + ContextInfo.period)
    # 设置账号
    ContextInfo.set_account('8881667160')
    print(ContextInfo.set_universe(['603444.SH']))
    # print('algorithms is running!')
    json_data = json.dumps(dir(ContextInfo))
    # r = requests.post('http://127.0.0.1:8000/init',json=json_data)
    # print(r)
    # 连接到服务器
    # client_socket.connect((server_host, server_port))
    # 启动接收数据的线程
    # receive_thread = threading.Thread(target=receive_data, args=(client_socket,message_queue))
    # receive_thread.setDaemon(True)
    # receive_thread.start()
    ContextInfo.set_universe(['603444.SH'])
    print(dir(ContextInfo))
    print('init success!')


def handlebar(ContextInfo):
    global a
    # 获取龙虎榜数据
    # print( ContextInfo.get_longhubang(['600336.SH'],'20231201','20140110'))
    # recv_data = message_queue.get()
    if not ContextInfo.is_last_bar():
        return
    # send_data(client_socket,'buy')
    # print(ContextInfo.get_bar_timetag(ContextInfo.barpos))
    # 获取最新分笔数据,实时行情
    Result = ContextInfo.get_full_tick(['603444.SH'])

    df = pd.DataFrame(Result)
    print()
    df2 = df.T
    df2.to_csv('603444SHTest.csv', mode='a')
    df.to_csv('603444SH.csv', mode='a')
    print('写入成功!')
    # uni = ContextInfo.get_universe()
    # for u in uni:
    #	passorder(23, 1101, '8881667160', u, 5, -1, 100, ContextInfo)  # 23买 # 24卖
    # 创建游标
    # cursor = conn.cursor()

    timetag = Result['603444.SH']['timetag']
    lastPrice = Result['603444.SH']['lastPrice']
    open = Result['603444.SH']['open']
    high = Result['603444.SH']['high']
    low = Result['603444.SH']['low']
    amount = Result['603444.SH']['amount']
    volume = Result['603444.SH']['volume']
    askPrice = Result['603444.SH']['askPrice']
    bidPrice = Result['603444.SH']['bidPrice']
    askVol = Result['603444.SH']['askVol']
    print(f'时间帧:{timetag}--总量:{volume}--askPrice:{askPrice}--bidPrice:{bidPrice}--askVol:{askVol}')
    print(f'开:{open}----交易手:{volume - a}---*--*---帧度：{(volume - a) * 100 * askPrice[0]:.2f}-----{(1 - (bidPrice[0] / open)) * 100:.3f}%--前:{bidPrice[0]}')
    # 执行 SQL 查询
    # cursor.execute(f"INSERT INTO data_info (id,code,name,date,volume,lastprice,high,low,amount,askprice,bidprice,askvol) VALUES ('{timetag}', '603444.SH','吉比特','{timetag}','{volume}','{lastPrice}','{high}','{low}','{amount}','{askPrice[0]}','{bidPrice[0]}','{askVol[0]}')")

    # 获取查询结果
    # result = cursor.fetchall()

    # 打印查询结果
    # for row in result:
    #	print(row)

    # 关闭游标和数据库连接
    # cursor.close()
    # hand = volume
    #
    # hisdict = ContextInfo.get_history_data(3, '1d', 'close')
    # for k, v in hisdict.items():
    #	if len(v) > 1:
    #		# 今日涨幅
    #		print(k, ':', v[1] - v[0])
    #		pass
    # 获取北向数据持股明细
    # ContextInfo.get_hkt_details('600336.SH')
    # 获取北向数据持股统计
    # ContextInfo.get_hkt_statistics('600336.SH')
    # 获取合约详细信息
    # print( ContextInfo.get_instrumentdetail('600336.SH'))
    # 获取行情数据
    # Result=ContextInfo.get_market_data_ex(
    # ['open', 'high', 'low', 'close'], ['000300.SH'], period='1d'
    # , start_time='', end_time='', count=-1
    # , dividend_type='follow', fill_data=True
    # , subscribe = True)
    # print(Result)
    index = ContextInfo.barpos


# 无风险利率
# print( ContextInfo.get_risk_free_rate(index))
# 取内盘成交量
# print( ContextInfo.get_svol('600336.SH'))
# 获取总股本
# print( ContextInfo.get_total_share('600336.SH'))
# 获取换手率数据
# print( ContextInfo.get_turnover_rate(['600336.SH'],'20240101','20240110'))
# 某只股票在某指数中的绝对权重
# print( ContextInfo.get_weight_in_index('000300.SH', '000002.SZ'))
# obj_list = get_trade_detail_data(ContextInfo.accid,'stock','position')
# for obj in obj_list:
#	print(obj.m_strInstrumentID)
#	print(dir(obj))
# acc_info = get_trade_detail_data(ContextInfo.accid,'stock','account')
# print(acc_info)
# orderid = 297
# print(orderid)
# obj = get_value_by_deal_id(orderid,ContextInfo.accid,'stock','deal')
# print(obj.m_strInstrumentID)
# 获取因子数据 get_factor_value()
# print(get_factor_value('zzz', '600000.SH', 0, ContextInfo))
# 获取引用的因子数据的数值在所有品种中排名 get_factor_rank()
# print(get_factor_rank('zzz', '600000.SH', 0, ContextInfo))
# realtimetag = ContextInfo.get_bar_timetag(ContextInfo.barpos)
# value = ContextInfo.get_close_price('','',realtimetag)
# ContextInfo.paint('close',value,-1,0,'white', 'noaxis')
# ContextInfo.draw_text(1,10,'测试文字啦啦啦')
# 在图形上显示数字
# close = ContextInfo.get_market_data(['close'])
# ContextInfo.draw_number(1>0, close,close,1)

# 资金账号状态变化主推
def account_callback(ContextInfo, accountInfo):
    pass


# 账号委托状态变化主推
def order_callback(ContextInfo, orderInfo):
    print('orderInfo')
    print(orderInfo)


# 账号成交状态变化主推
def deal_callback(ContextInfo, dealInfo):
    print('发生交易')
    print(dealInfo)


# 账号异常下单主推
def position_callback(ContextInfo, orderArgs):
    print('orderArgs')


def myHandlebar(ContextInfo):
    print('hello world')

