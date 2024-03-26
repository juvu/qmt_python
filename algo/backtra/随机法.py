import random


def generate_random_number():
    # 生成随机数
    random_number = random.uniform(-0.1, 0.1)

    # 将随机数四舍五入到小数点后四位
    random_number = round(random_number, 4)

    # 生成一个0到1之间的随机数
    probability = random.random()

    # 根据概率判断是否将随机数转为正数
    if probability < 0.1:
        random_number = abs(random_number)

    return random_number


# 调用函数生成随机数

principal = 70000
fund = 70000
out = 60000
trade_date=200
stop_loss = -0.05
for i in range(trade_date):
    random_num = generate_random_number()
    yield_rate = fund / principal
    if random_num < stop_loss:
        random_num = stop_loss

    fund*=1+random_num
    print(fund)
    if fund <= out:
        break

print(f'经过{i}个交易日后，{fund}')