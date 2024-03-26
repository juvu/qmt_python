#coding:gbk

class a():pass
A = a()
A.bought_list = []

account = '8881667160'
def init(C):
	#下单函数的参数需要 ContextInfo对象 在init中定义行情回调函数 可以用到init函数的入参 不用手动传入
	def callback_func(data):
		#print(data)
		for stock in data:
			current_price = data[stock]['close']
			pre_price = data[stock]['preClose']
			ratio = current_price / pre_price - 1
			print(stock, C.get_stock_name(stock), '当前涨幅', ratio)
			#if ratio > 0 and stock not in A.bought_list:
			if stock not in A.bought_list:
				msg = f"当前涨幅 {ratio} 大于0 买入100股"
				print(msg)
				#下单函数passorder 安全起见处于注释状态 需要实际测试下单交易时再放开
				#passorder(23, 1101, account, stock, 5, -1, 100, '订阅下单示例', 2, msg, C)
				A.bought_list.append(stock)
	stock_list = ['600000.SH', '000001.SZ']
	for stock in stock_list:
		C.subscribe_quote(stock, period = '1d', callback = callback_func)

