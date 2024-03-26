import pandas as pd
import matplotlib.pyplot as plt

# 假设有一份股价数据，其中包括日期和收盘价
# 这里只是一个简单的示例，你需要用你自己的数据替代
df = pd.read_csv('603444.csv')
print(df.tail(40))
df = df.tail(360)
# df = pd.DataFrame(data)
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)

# 计算布林线指标
# 这里使用了简单移动平均线（SMA）和标准差来计算上下轨道
df['SMA'] = df['close'].rolling(window=20).mean()
df['Upper'] = df['SMA'] + 2 * df['close'].rolling(window=20).std()
df['Lower'] = df['SMA'] - 2 * df['close'].rolling(window=20).std()

# 绘制布林线图
plt.figure(figsize=(10, 6))
plt.plot(df['close'], label='close Price', color='blue')
plt.plot(df['SMA'], label='20-day SMA', color='orange')
plt.plot(df['Upper'], label='high Band', linestyle='--', color='red')
plt.plot(df['Lower'], label='low Band', linestyle='--', color='green')

plt.title('Bollinger Bands')
plt.xlabel('date')
plt.ylabel('Price')
plt.legend()
plt.show()
