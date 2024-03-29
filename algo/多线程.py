'''
Date: 2024-03-25 08:38:42
LastEditors: 牛智超
LastEditTime: 2024-03-29 13:38:29
FilePath: \python\algo\多线程.py
'''
import os
import threading

import akshare as ak
import multiprocessing
import numpy as np
import time

start_time = time.time()

today = time.strftime("%Y%m%d", time.localtime())
if os.path.exists(f'./algo/stock/{today}') == False:
    os.makedirs(f'./algo/stock/{today}')


def splite_data(data):
    return np.array_split(data, 4)


def build_csv(data):
    for i in data:
        try:
            stock_history = ak.stock_zh_a_hist(symbol=i, period='daily', adjust='', start_date="20220301", end_date=today).iloc[:, 0:6]

            # 列名
            stock_history.columns = [
                'date',
                'open',
                'close',
                'high',
                'low',
                'volume',
            ]
            # 对列进行重新排序设置成OHLC
            stock_history = stock_history[['date', 'open', 'high', 'low', 'close', 'volume']]

            # 设置以日期为索引
            stock_history.set_index('date', drop=True, inplace=True)

            # 保存成csv文件，这里可以设置自己的路径。
            print(i)
            stock_history.to_csv(f'./algo/stock/{today}/{i}.csv')
        except:
            continue


# 获取所有的股票代码
stockname = ak.stock_zh_a_spot_em()
df = stockname['代码']

df = splite_data(df)

threads = []
for i in range(4):
    t = threading.Thread(target=build_csv, args=(df[i],))
    threads.append(t)
    t.start()

for thread in threads:
    thread.join()

end_time = time.time()

print(end_time - start_time)
