import matplotlib.pyplot as plt
import numpy as np

plt.title("标题")#括号当中输入标题的名称
plt.rcParams['font.sans-serif']=['SimHei']
# plt.figure(figsize=(6, 3))
plt.plot(6, 3,label='123')
plt.plot(3, 3 *2, label='456')
plt.legend(loc='best')#图列位置，可选best，center等
x = np.linspace(0,10,200)
y = np.sin(x)
plt.plot(x,y,linestyle=":",color='b')
plt.annotate("注释", xy=(2, 8), xytext=(3, 9), arrowprops=dict(facecolor='black', shrink=0.05))
plt.show()