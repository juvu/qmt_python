#coding=utf-8
from xtquant.xttrader import XtQuantTrader, XtQuantTraderCallback
from xtquant.xttype import StockAccount
from xtquant import xtconstant


class MyXtQuantTraderCallback(XtQuantTraderCallback):
    def on_disconnected(self):
        """
        连接断开
        :return:
        """
        print("connection lost")
    def on_stock_order(self, order):
        """
        委托回报推送
        :param order: XtOrder对象
        :return:
        """
        print("on order callback:")
        print(order.stock_code, order.order_status, order.order_sysid)
    def on_stock_asset(self, asset):
        """
        资金变动推送  注意，该回调函数目前不生效
        :param asset: XtAsset对象
        :return:
        """
        print("on asset callback")
        print(asset.account_id, asset.cash, asset.total_asset)
    def on_stock_trade(self, trade):
        """
        成交变动推送
        :param trade: XtTrade对象
        :return:
        """
        print("on trade callback")
        print(trade.account_id, trade.stock_code, trade.order_id)
    def on_stock_position(self, position):
        """
        持仓变动推送  注意，该回调函数目前不生效
        :param position: XtPosition对象
        :return:
        """
        print("on position callback")
        print(position.stock_code, position.volume)
    def on_order_error(self, order_error):
        """
        委托失败推送
        :param order_error:XtOrderError 对象
        :return:
        """
        print("on order_error callback")
        print(order_error.order_id, order_error.error_id, order_error.error_msg)
    def on_cancel_error(self, cancel_error):
        """
        撤单失败推送
        :param cancel_error: XtCancelError 对象
        :return:
        """
        print("on cancel_error callback")
        print(cancel_error.order_id, cancel_error.error_id, cancel_error.error_msg)
    def on_order_stock_async_response(self, response):
        """
        异步下单回报推送
        :param response: XtOrderResponse 对象
        :return:
        """
        print("on_order_stock_async_response")
        print(response.account_id, response.order_id, response.seq)
    def on_account_status(self, status):
        """
        :param response: XtAccountStatus 对象
        :return:
        """
        print("on_account_status")
        print(status.account_id, status.account_type, status.status)
['__class__', '__deepcopy__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'barpos', 'benchmark', 'bsm_iv', 'bsm_price', 'capital', 'context', 'create_sector', 'current_bar', 'data_info_level', 'dividend_type', 'do_back_test', 'draw_icon', 'draw_number', 'draw_text', 'draw_vertline', 'end', 'get_ETF_list', 'get_all_subscription', 'get_back_test_index', 'get_bar_timetag', 'get_bvol', 'get_close_price', 'get_commission', 'get_contract_expire_date', 'get_contract_multiplier', 'get_date_location', 'get_divid_factors', 'get_factor_data', 'get_finance', 'get_financial_data', 'get_float_caps', 'get_full_tick', 'get_function_line', 'get_his_contract_list', 'get_his_index_data', 'get_his_st_data', 'get_history_data', 'get_hkt_details', 'get_hkt_statistics', 'get_holder_num', 'get_industry', 'get_instrumentdetail', 'get_largecap', 'get_last_close', 'get_last_volume', 'get_local_data', 'get_longhubang', 'get_main_contract', 'get_market_data', 'get_market_data_ex', 'get_market_data_ex_ori', 'get_midcap', 'get_net_value', 'get_north_finance_change', 'get_open_date', 'get_option_detail_data', 'get_option_iv', 'get_option_list', 'get_option_undl', 'get_option_undl_data', 'get_product_asset_value', 'get_product_init_share', 'get_product_share', 'get_raw_financial_data', 'get_risk_free_rate', 'get_scale_and_rank', 'get_scale_and_stock', 'get_sector', 'get_slippage', 'get_smallcap', 'get_stock_list_in_sector', 'get_stock_name', 'get_stock_type', 'get_svol', 'get_tick_timetag', 'get_top10_share_holder', 'get_total_share', 'get_tradedatafromerds', 'get_trading_dates', 'get_turn_over_rate', 'get_turnover_rate', 'get_universe', 'get_weight_in_index', 'in_pythonworker', 'is_fund', 'is_future', 'is_last_bar', 'is_new_bar', 'is_stock', 'is_suspended_stock', 'load_stk_list', 'load_stk_vol_list', 'market', 'paint', 'period', 'refresh_rate', 'request_id', 'run_time', 'set_account', 'set_commission', 'set_slippage', 'set_universe', 'start', 'stockcode', 'stockcode_in_rzrk', 'subMap', 'subscribe_quote', 'subscribe_whole_quote', 'time_tick_size', 'unsubscribe_quote', 'z8sglma_last_barpos', 'z8sglma_last_version']
if __name__ == "__main__":
    print("demo test")
    # path为mini qmt客户端安装目录下userdata_mini路径
    path = 'E:\\国金证券QMT交易端\\bin.x64'
    # session_id为会话编号，策略使用方对于不同的Python策略需要使用不同的会话编号
    session_id = 123456
    xt_trader = XtQuantTrader(path, session_id)
    # 开启主动请求接口的专用线程 开启后在on_stock_xxx回调函数里调用XtQuantTrader.query_xxx函数不会卡住回调线程，但是查询和推送的数据在时序上会变得不确定
    # 详见: http://docs.thinktrader.net/vip/pages/ee0e9b/#开启主动请求接口的专用线程
    # xt_trader.set_relaxed_response_order_enabled(True)
    # 创建资金账号为1000000365的证券账号对象
    acc = StockAccount('8881667160')
    # StockAccount可以用第二个参数指定账号类型，如沪港通传'HUGANGTONG'，深港通传'SHENGANGTONG'
    # acc = StockAccount('1000000365','STOCK')
    # 创建交易回调类对象，并声明接收回调
    callback = MyXtQuantTraderCallback()
    xt_trader.register_callback(callback)
    # 启动交易线程
    xt_trader.start()
    # 建立交易连接，返回0表示连接成功
    connect_result = xt_trader.connect()
    if connect_result != 0:
        import sys
        sys.exit('链接失败，程序即将退出 %d'%connect_result)
    # 对交易回调进行订阅，订阅后可以收到交易主推，返回0表示订阅成功
    subscribe_result = xt_trader.subscribe(acc)
    if subscribe_result != 0:
        print('账号订阅失败 %d'%subscribe_result)
    print(subscribe_result)
    stock_code = '600000.SH'
    # 使用指定价下单，接口返回订单编号，后续可以用于撤单操作以及查询委托状态
    print("order using the fix price:")
    fix_result_order_id = xt_trader.order_stock(acc, stock_code, xtconstant.STOCK_BUY, 200, xtconstant.FIX_PRICE, 10.5, 'strategy_name', 'remark')
    print(fix_result_order_id)
    # 使用订单编号撤单
    print("cancel order:")
    cancel_order_result = xt_trader.cancel_order_stock(acc, fix_result_order_id)
    print(cancel_order_result)
    # 使用异步下单接口，接口返回下单请求序号seq，seq可以和on_order_stock_async_response的委托反馈response对应起来
    print("order using async api:")
    async_seq = xt_trader.order_stock(acc, stock_code, xtconstant.STOCK_BUY, 200, xtconstant.FIX_PRICE, 10.5, 'strategy_name', 'remark')
    print(async_seq)
    # 查询证券资产
    print("query asset:")
    asset = xt_trader.query_stock_asset(acc)
    if asset:
        print("asset:")
        print("cash {0}".format(asset.cash))
    # 根据订单编号查询委托
    print("query order:")
    order = xt_trader.query_stock_order(acc, fix_result_order_id)
    if order:
        print("order:")
        print("order {0}".format(order.order_id))
    # 查询当日所有的委托
    print("query orders:")
    orders = xt_trader.query_stock_orders(acc)
    print("orders:", len(orders))
    if len(orders) != 0:
        print("last order:")
        print("{0} {1} {2}".format(orders[-1].stock_code, orders[-1].order_volume, orders[-1].price))
    # 查询当日所有的成交
    print("query trade:")
    trades = xt_trader.query_stock_trades(acc)
    print("trades:", len(trades))
    if len(trades) != 0:
        print("last trade:")
        print("{0} {1} {2}".format(trades[-1].stock_code, trades[-1].traded_volume, trades[-1].traded_price))
    # 查询当日所有的持仓
    print("query positions:")
    positions = xt_trader.query_stock_positions(acc)
    print("positions:", len(positions))
    if len(positions) != 0:
        print("last position:")
        print("{0} {1} {2}".format(positions[-1].account_id, positions[-1].stock_code, positions[-1].volume))
    # 根据股票代码查询对应持仓
    print("query position:")
    position = xt_trader.query_stock_position(acc, stock_code)
    if position:
        print("position:")
        print("{0} {1} {2}".format(position.account_id, position.stock_code, position.volume))
    # 阻塞线程，接收交易推送
    xt_trader.run_forever()
