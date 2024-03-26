import easyquotation

quotation = easyquotation.use('tencent')  # 新浪 ['sina'] 腾讯 ['tencent', 'qq']

# 获取所有股票行情
# all_data = quotation.market_snapshot(prefix=True)  # prefix 参数指定返回的行情字典中的股票代码 key 是否带 sz/sh 前缀

# # 单只股票
# one_data = quotation.real('162411')  # 支持直接指定前缀，如 'sh000001'
#
# # 多只股票
# many_data = quotation.stocks(['000001', '162411'])
#
# # 同时获取指数和行情
part_data = quotation.stocks(['sh000001', 'sz000001'], prefix=True)
print(part_data)
# print(all_data)