#coding:utf-8
from functools import wraps
import copy
import traceback
import time

hint_get_history_data = True
hint_get_market_data = True
hint_get_local_data = True

class __PyContext(object):
    def __init__(self, contextinfo=None):
        self.context = contextinfo
        self.z8sglma_last_version = None
        self.z8sglma_last_barpos = -1
        self.subMap = {}

    def set_account(self, acct):
        self.context.set_account(acct)

    def set_universe(self, universe):
        last_universe = self.context.get_universe();
        universe = list(set(universe).difference(set(last_universe)));
        self.context.set_universe(universe)

    def get_universe(self):
        return self.context.get_universe()
    
    def is_last_bar(self):
        return self.context.is_last_bar()

    def is_new_bar(self):
        return self.context.is_new_bar()
    
    def get_history_data(self, len, period, field, dividend_type='none', skip_paused=True):
        global hint_get_history_data
        if hint_get_history_data:
            print ("get_history_data接口版本较老，推荐使用get_market_data_ex替代，配合download_history_data补充昨日以前的历史数据")
            hint_get_history_data = False
        return self.context.get_history_data(len, period, field, dividend_type, skip_paused)
    
    def get_industry(self, industry_name, real_timetag = -1):
        return self.context.get_industry(industry_name, real_timetag)

    def get_last_close(self,stock):
        return self.context.get_last_close(stock)

    def get_last_volume(self,stock):
        return self.context.get_last_volume(stock)
    
    def get_sector(self, sectorname, real_timetag = -1):
        return self.context.get_sector(sectorname, real_timetag)

    def get_scale_and_stock(self, total, stockValue, stock):
        return self.context.get_scale_and_stock(total, stockValue, stock)
    def get_scale_and_rank(self,list):
        return self.context.get_scale_and_rank(list)
		
    def get_finance(self, vStock):
        return self.context.get_finance(vStock)
		
    def get_smallcap(self):
        return self.context.get_smallcap()

    def get_midcap(self):
        return self.context.get_midcap()
    
    def get_largecap(self):
        return self.context.get_largecap()
        
    def get_bar_timetag(self, index):
        return self.context.get_bar_timetag(index)

    def get_tick_timetag(self):
        return self.context.get_tick_timetag()

    def get_risk_free_rate(self, index):
        return self.context.get_risk_free_rate(index)

    def get_contract_multiplier(self, stockcode):
        return self.context.get_contract_multiplier(stockcode)
    
    def get_float_caps(self, stockcode):
        return self.context.get_float_caps(stockcode)
    
    def get_total_share(self, stockcode):
        return self.context.get_total_share(stockcode)
    
    def get_stock_type(self, stock):
        return self.context.get_stock_type(stock)

    def get_stock_name(self, stock):
        return self.context.get_stock_name(stock)

    def get_open_date(self, stock):
        return self.context.get_open_date(stock)

    def get_contract_expire_date(self, stock):
        return str(self.context.get_contract_expire_date(stock))

    def get_svol(self, stock):
        return self.context.get_svol(stock)

    def get_bvol(self, stock):
        return self.context.get_bvol(stock)

    def get_net_value(self, barpositon):
        return self.context.get_net_value(barpositon)
    
    def get_back_test_index(self):
        return self.context.get_back_test_index()
    
    def get_turn_over_rate(self, stockcode):
        return self.context.get_turn_over_rate(stockcode) 
    
    def get_weight_in_index(self, mtkindexcode, stockcode):
        return self.context.get_weight_in_index(mtkindexcode, stockcode)
    
    def get_stock_list_in_sector(self, sectorname, real_timetag = -1):
        if isinstance(real_timetag,str):
            real_timetag = int(time.mktime(time.strptime(real_timetag, '%Y%m%d'))*1000)
        if real_timetag == -1:
            return get_stock_list_in_sector(sectorname)
        return self.context.get_stock_list_in_sector(sectorname, real_timetag)
        
    def get_tradedatafromerds(self, accounttype, accountid, startdate, enddate):
        return self.context.get_tradedatafromerds(accounttype ,accountid, startdate, enddate)

    def get_close_price(self, market, stockCode, realTimetag, period=86400000, dividType=0):
        return self.context.get_close_price(market, stockCode, realTimetag, period, dividType)

    def get_market_data_ex(self, fields=[], stock_code=[], period='follow', start_time='', end_time='', count=-1,
                         dividend_type='follow', fill_data=True, subscribe=True):
        ori_data = self.context.get_market_data2(
            fields
            , stock_code, period
            , start_time, end_time, count
            , dividend_type, fill_data
            , subscribe
        )
        
        import pandas as pd
        result = {}
        
        ifield = 'stime'
        fl = fields
        if fl:
            fl2 = fl if ifield in fl else [ifield] + fl
            for s in ori_data:
                sdata = pd.DataFrame(ori_data[s], columns = fl2)
                sdata2 = sdata[fl]
                sdata2.index = sdata[ifield]
                result[s] = sdata2
        else:
            for s in ori_data:
                sdata = pd.DataFrame(ori_data[s])
                if ifield in sdata:
                    sdata.index = sdata[ifield]
                result[s] = sdata
        
        return result

    def get_market_data_ex_ori(self, fields=[], stock_code=[], period='follow', start_time='', end_time='', count=-1,
                         dividend_type='follow', fill_data=True, subscribe=True):
        oriData = self.context.get_market_data2(
            fields
            , stock_code, period
            , start_time, end_time, count
            , dividend_type, fill_data
            , subscribe
        )
        return oriData

    def get_market_data(self, fields, stock_code=[], start_time='', end_time='', skip_paused=True, period='follow',
                        dividend_type='follow', count=-1):
        global hint_get_market_data
        if hint_get_market_data:
            print ("get_market_data接口版本较老，推荐使用get_market_data_ex替代，配合download_history_data补充昨日以前的历史数据")
            hint_get_market_data = False
        oriData = self.context.get_market_data(fields, stock_code, start_time, end_time, skip_paused, period,dividend_type, count)
        resultDict = {}
        for code in oriData:
            for timenode in oriData[code]:
                values=[]
                for field in fields:
                    values.append(oriData[code][timenode][field])
                key=code+timenode
                resultDict[key]=values
        if len(fields)==1 and len(stock_code)<=1 and ((start_time=='' and end_time=='') or start_time==end_time) and count==-1:
            for key in resultDict:
                return resultDict[key][0]
            return -1
        import numpy as np
        import pandas as pd
        if len(stock_code)<=1 and start_time=='' and end_time=='' and count==-1:
            for key in resultDict:
                result=pd.Series(resultDict[key],index=fields)
                return result.sort_index()
        if len(stock_code)>1 and start_time=='' and end_time=='' and count==-1:
            values=[]
            for code in stock_code:
                if code in oriData:
                    if not oriData[code]:
                        values.append([np.nan])
                    for timenode in oriData[code]:
                        key=code+timenode
                        values.append(resultDict[key])
                else:
                    values.append([np.nan])
            result=pd.DataFrame(values,index=stock_code,columns=fields)
            return result.sort_index()
        if len(stock_code)<=1 and ((start_time!='' or end_time!='') or count>=0):
            values=[]
            times=[]
            for code in oriData:
                for timenode in oriData[code]:
                    key=code+timenode
                    times.append(timenode)
                    values.append(resultDict[key])
            result=pd.DataFrame(values,index=times,columns=fields)
            return result.sort_index()
        if len(stock_code)>1 and ((start_time!='' or end_time!='') or count>=0):
            values={}
            for code in stock_code:
                times=[]
                value=[]
                if code in oriData:
                    for timenode in oriData[code]:
                        key=code+timenode
                        times.append(timenode)
                        value.append(resultDict[key])
                values[code]=pd.DataFrame(value,index=times,columns=fields).sort_index()
            result=pd.Panel(values)
            return result
        return

    def get_full_tick(self, stock_code=[]):
        return self.context.get_full_tick(stock_code)
    def get_north_finance_change(self, period):
        return self.context.get_north_finance_change(period)
    def get_hkt_statistics(self, stock_code):
        return self.context.get_hkt_statistics(stock_code)
    def get_hkt_details(self, stock_code):
        return self.context.get_hkt_details(stock_code)
    def load_stk_list(self, dirfile, namefile):
        return self.context.load_stk_list(dirfile, namefile)
    def load_stk_vol_list(self, dirfile, namefile):
        return self.context.load_stk_vol_list(dirfile, namefile)
    def get_longhubang(self, stock_list=[], startTime='', endTime='', count=-1):
        import pandas as pd
        resultDf = pd.DataFrame()
        if isinstance(endTime, int):
            count = endTime
            endTime = startTime
            startTime = '0'
        else:
            count = -1
        resultDict = self.context.get_longhubang(stock_list, startTime, endTime, count)
        fields = ['stockCode', 'stockName', 'date', 'reason', 'close', 'SpreadRate', 'TurnoverVolume',
                  'Turnover_Amount', "buyTraderBooth", "sellTraderBooth"]
        tradeBoothItemFiled = ["traderName", "buyAmount", "buyPercent", "sellAmount", "sellPercent", "totalAmount",
                               "rank", "direction"]
        for stock in resultDict:
            stockDict = resultDict[stock]
            stockDf = pd.DataFrame()
            if len(stockDict.keys()) < 10:
                continue
            buyTradeBoothDict = stockDict[8]
            sellTradeBoothDict = stockDict[9]
            buyTradeBoothPdList = []
            sellTradeBoothPdList = []
            for TradeBoothIDict in buyTradeBoothDict:
                buyTradeBoothPd = pd.DataFrame()
                for tradeBoothKey in TradeBoothIDict.keys():
                    buyTradeBoothPd[tradeBoothItemFiled[tradeBoothKey]] = TradeBoothIDict[tradeBoothKey]
                buyTradeBoothPdList.append(buyTradeBoothPd)
            for TradeBoothIDict in sellTradeBoothDict:
                sellTradeBoothPd = pd.DataFrame()
                for tradeBoothKey in TradeBoothIDict.keys():
                    sellTradeBoothPd[tradeBoothItemFiled[tradeBoothKey]] = TradeBoothIDict[tradeBoothKey]
                sellTradeBoothPdList.append(sellTradeBoothPd)
            for i in range(0, 8):
                stockDf[fields[i]] = stockDict[i]
            stockDf[fields[8]] = buyTradeBoothPdList
            stockDf[fields[9]] = sellTradeBoothPdList
            resultDf = resultDf.append(stockDf)
        return resultDf

    def get_main_contract(self, codemarket):
        return self.context.get_main_contract(codemarket)

    def get_his_contract_list(self, market):
            return get_his_contracts_list(market);

    def get_date_location(self, date):
        return self.context.get_date_location(date)
    
    def get_product_share(self, code, index=-1):
        return self.context.get_product_share(code, index)

    def get_divid_factors(self, marketAndStock, date = ''):
        return self.context.get_divid_factors(marketAndStock,date)

    def get_financial_data(self, fieldList, stockList, startDate, endDate, report_type = 'report_time', pos = -1):
        if(type(report_type) != str):   # default value error , report_type -> pos 
            pos = report_type;
            report_type = 'report_time';
        if(report_type != 'announce_time' and report_type != 'report_time'):
            return;

    def get_raw_financial_data(self, fieldList, stockList, startDate, endDate, report_type='report_time',data_type='dict'):
        if (report_type != 'announce_time' and report_type != 'report_time'):
            return
        import pandas as pd
        from collections import OrderedDict
        pandasData = self.context.get_financial_data(fieldList, stockList, startDate, endDate, report_type, data_type, True)
        return pandasData;

    def get_financial_data(self, fieldList, stockList, startDate, endDate, report_type='report_time', pos=-1):
        if (type(report_type) != str):  # default value error , report_type -> pos
            pos = report_type
            report_type = 'report_time'
        if (report_type != 'announce_time' and report_type != 'report_time'):
            return
        if type(fieldList) == str and type(stockList) == str:
            return self.context.get_financial_data(fieldList, stockList, startDate, endDate, report_type, pos);
        import pandas as pd
        from collections import OrderedDict
        
        pandasData = self.context.get_financial_data(fieldList, stockList, startDate, endDate, report_type,'dict',False)
        if not pandasData:
            return
        fields = pandasData['field']
        stocks = pandasData['stock']
        dates = pandasData['date']
        values = pandasData['value']

        if len(stocks) == 1 and len(dates) == 1:    #series
            series_list = []
            for value in values:
                if not value:
                    return
                for subValue in value:
                    series_list.append(subValue)
            return pd.Series(series_list, index = fields)
        elif len(stocks) == 1 and len(dates) > 1:   #index = dates, col = fields
            dataDict = OrderedDict()
            for n in range(len(values)):
                dataList = []
                if not values[n]:
                    return
                for subValue in values[n]:
                    dataList.append(subValue)
                dataDict[fields[n]] = pd.Series(dataList, index = dates)
            return pd.DataFrame(dataDict)
        elif len(stocks) > 1 and len(dates) == 1:   #index = stocks col = fields
            dataDict = OrderedDict()
            for n in range(len(values)):
                dataList = []
                if not values[n]:
                    return
                for subValue in values[n]:
                    dataList.append(subValue)
                dataDict[fields[n]] = pd.Series(dataList, index = stocks)
            return pd.DataFrame(dataDict)
        else:                                       #item = stocks major = dates minor = fields
            panels = OrderedDict()
            for i in range(len(stocks)):
                dataDict = OrderedDict()
                for j in range(len(values)):
                    dataList = []
                    value = values[j]
                    if not value:
                        return
                    for k in range(i * len(dates), (i + 1) * len(dates)):
                        dataList.append(value[k])
                    dataDict[fields[j]] = pd.Series(dataList, index = dates)
                panels[stocks[i]] = pd.DataFrame(dataDict)
            return pd.Panel(panels)
            
    def get_top10_share_holder(self, stock_list, data_name,start_time,end_time, report_type='report_time'):
        import pandas as pd
        resultPanelDict = {}
        resultDict ={}
        if (report_type != 'announce_time' and report_type != 'report_time'):
            return "input report_type = \'report_time\' or report_type = \'announce_time\'"
        if(data_name == 'flow_holder' or data_name == 'holder'):
            resultDict = get_top10_holder(stock_list, data_name, start_time, end_time, report_type);
        else:
            return "input data_name = \'flow_holder\' or data_name = \'holder\'"
        fields = ["holdName","holderType","holdNum","changReason","holdRatio","stockType","rank","status","changNum","changeRatio"]
        for stock in resultDict:
            stockPdData = pd.DataFrame(columns = fields)
            stockDict = resultDict[stock]
            for timeKey in list(stockDict.keys()):
                timelist = stockDict[timeKey]
                stockPdData.loc[timeKey] =  timelist
            resultPanelDict[stock] = stockPdData
        resultPanel = pd.Panel(resultPanelDict)
        stockNum = len(stock_list)
        timeNum = len(resultPanel.major_axis)
        if(stockNum == 1 and timeNum == 1):
            stock = resultPanel.items[0]
            timetag = resultPanel.major_axis[0]
            df = pd.DataFrame(resultPanel[stock])
            result = pd.Series(df.ix[timetag],index = fields)
            return result
        elif(stockNum > 1 and timeNum == 1):
            timetag = resultPanel.major_axis[0]
            result = pd.DataFrame(resultPanel.major_xs(timetag),index =  fields,columns = resultPanel.items);
            result = result.T
            return  result
        elif(stockNum == 1 and timeNum > 1):
            stock = resultPanel.items[0]
            result = pd.DataFrame(resultPanel[stock])
            return result
        elif(stockNum > 1 and timeNum > 1):
            return resultPanel
        return pd.Panel()
    def get_product_asset_value(self, code, index=-1):
        return self.context.get_product_asset_value(code, index)

    def get_product_init_share(self,code=''):
        return self.context.get_product_init_share(code)

    def create_sector(self, sectorname, stocklist):
        return self.context.create_sector(sectorname, stocklist)    
    def get_holder_num(self, stock_list =[], startTime = '', endTime = '', report_type = 'report_time'):
        fields = ["stockCode","timetag","holdNum","AHoldNum","BHoldNum","HHoldNum","uncirculatedHoldNum","circulatedHoldNum"];
        if (report_type != 'announce_time' and report_type != 'report_time'):
            return "input report_type = \'report_time\' or report_type = \'announce_time\'"
        import pandas as pd
        resultDict = get_holder_number(stock_list, startTime, endTime, report_type)
        result  =  pd.DataFrame()
        for stock in resultDict:
            df = pd.DataFrame(columns = fields)
            for i in  resultDict[stock]:
                df[fields[i]]=resultDict[stock][i]
            result = result.append(df)
        return  result
        
    def paint(self, name, data, index, drawStyle, selectcolor='', limit=''):
        selectcolor_low = selectcolor.lower()
        limit_low = limit.lower()
        if '' != selectcolor and 'noaxis' == limit_low:
            return self.context.paint(name, data, index, drawStyle, selectcolor, 0)
        elif '' != selectcolor and 'nodraw' == limit_low:
            return self.context.paint(name, data, index, 7, selectcolor, 0)
        elif 'noaxis' == selectcolor_low:
            return self.context.paint(name, data, index, drawStyle, '', 0)
        elif 'nodraw' == selectcolor_low:
            return self.context.paint(name, data, index, 7, '', 0)
        else:
            return self.context.paint(name, data, index, drawStyle, selectcolor_low, 1)

    def set_slippage(self, b_flag, slippage='none'):
        if slippage != 'none':
            self.context.set_slippage(b_flag,slippage)
        else:
            self.context.set_slippage(b_flag)#b_flag=slippage
            
    
    def get_slippage(self):
        return self.context.get_slippage()
    
    def get_commission(self):
        return self.context.get_commission()

    def set_commission(self,comtype,com='none'):
        if com != 'none':
           self.context.set_commission(comtype,com)
        else:
           self.context.set_commission(0,comtype)#comtype=commission
    
    def is_suspended_stock(self, stock, type = 0):
        return self.context.is_suspended_stock(stock, type)

    def is_stock(self,stock):
        return self.context.is_stock(stock)

    def is_fund(self,stock):
        return self.context.is_fund(stock)

    def is_future(self,market):
        return self.context.is_future(market)

    def run_time(self, funcname, intervalday, time, exchange = "SH"):
        self.context.run_time(funcname, intervalday, time, exchange)

    def get_function_line(self):
        import sys
        return sys._getframe().f_back.f_lineno
        
    def get_trading_dates(self, stockcode, start_date, end_date, count, period='1d'):
        return self.context.get_trading_dates(stockcode, start_date, end_date, count, period)

    def draw_text(self, condition, position, text, limit=''):
        import sys
        line = sys._getframe().f_back.f_lineno
        if 'noaxis' == limit.lower():
            return self.context.draw_text(condition, position, text, line, 0)
        else:
            return self.context.draw_text(condition, position, text, line, 1)

    def draw_vertline(self, condition, price1, price2, color='', limit=''):
        import sys
        line = sys._getframe().f_back.f_lineno

        if 'noaxis' == limit.lower():
            return self.context.draw_vertline(condition, price1, price2, color, line, 0)
        else:
            return self.context.draw_vertline(condition, price1, price2, color, line, 1)

    def draw_icon(self, condition, position, type, limit=''):
        import sys
        line = sys._getframe().f_back.f_lineno
        if (('noaxis' == limit.lower())):
            return self.context.draw_icon(condition, position, type, line, 0)
        else:
            return self.context.draw_icon(condition, position, type, line, 1)

    def draw_number(self, cond, price, number, precision, limit=''):
        import sys
        line = sys._getframe().f_back.f_lineno
        if (('noaxis' == limit.lower())):
            return self.context.draw_number(cond, price, number, precision, line, 0)
        else:
            return self.context.draw_number(cond, price, number, precision, line, 1)
        
    def get_turnover_rate(self, stock_code=[], start_time='19720101', end_time='22010101'):
        import pandas as pd
        import time
        if(len(start_time) != 8 or len(end_time) != 8):
            print('input date time error!!!')
            return pd.DataFrame()
        data = turnover_rate(stock_code, start_time, end_time)
        frame = pd.DataFrame(data)
        
        return frame;

    def get_local_data(self, stock_code='', start_time='19700101', end_time='22010101', period='follow', divid_type='none', count=-1):
        global hint_get_local_data
        if hint_get_local_data:
            print ("get_local_data接口版本较老，推荐使用get_market_data_ex替代，参数subscribe设置为False，只取本地数据不从服务器订阅数据")
            hint_get_local_data = False
        return self.context.get_local_data(stock_code, start_time, end_time, period, divid_type, count)
        
    def get_ETF_list(self, market, stockcode, typeList = []):
        import pandas as pd
        if(len(market) == 0):
            print('input market error!!!')
            return pd.DataFrame()
        data = get_etf_list(market, stockcode, typeList)
        frame = pd.DataFrame(data)
        
        return data;
        
    def get_option_detail_data(self, stockcode):
        return self.context.get_option_detail_data(stockcode)
        
    def get_instrumentdetail(self, marketCode):
        field_list = [
            'ExchangeID'
            , 'InstrumentID'
            , 'InstrumentName'
            , 'ProductID'
            , 'ProductName'
            , 'CreateDate'
            , 'OpenDate'
            , 'ExpireDate'
            , 'PreClose'
            , 'SettlementPrice'
            , 'UpStopPrice'
            , 'DownStopPrice'
            , 'FloatVolumn'
            , 'TotalVolumn'
            , 'LongMarginRatio'
            , 'ShortMarginRatio'
            , 'PriceTick'
            , 'VolumeMultiple'
            , 'MainContract'
            , 'LastVolume'
            , 'InstrumentStatus'
            , 'IsTrading'
            , 'IsRecent'
            , 'HSGTFlag'
        ]

        inst = self.context.get_instrumentdetail(marketCode)

        ret = {}
        for field in field_list:
            ret[field] = inst.get(field)
        return ret

    
    def get_option_undl(self, opt_code):
        inst = self.context.get_instrumentdetail(opt_code)
        if inst and 'ExtendInfo' in inst:
            ext_info = inst['ExtendInfo']
            undl_code_ref = str(ext_info['OptUndlCode']) + '.' + str(ext_info['OptUndlMarket'])
            if opt_code.find(".IF") != -1:
                if undl_code_ref == "000016.SH" or undl_code_ref == "000300.SH" or undl_code_ref == "000852.SH" or undl_code_ref == "000905.SH":
                    return undl_code_ref
            else:
                return undl_code_ref
        return

    def get_option_undl_data(self, undl_code_ref = ''):
        if undl_code_ref:
            opt_list = []
            if undl_code_ref.endswith('.SH'):
                if undl_code_ref == "000016.SH" or undl_code_ref == "000300.SH" or undl_code_ref == "000852.SH" or undl_code_ref == "000905.SH":
                    opt_list = get_stock_list_in_sector('中金所')
                else:
                    opt_list = self.get_stock_list_in_sector('上证期权')
            if undl_code_ref.endswith('.SZ'):
                opt_list = self.get_stock_list_in_sector('深证期权')
            data = []
            for opt_code in opt_list:
                undl_code = self.get_option_undl(opt_code)
                if undl_code == undl_code_ref:
                    data.append(opt_code)
            return data
        else:
            opt_list = []
            opt_list += self.get_stock_list_in_sector('上证期权')
            opt_list += self.get_stock_list_in_sector('深证期权')
            opt_list += self.get_stock_list_in_sector('中金所')
            result = {}
            for opt_code in opt_list:
                undl_code = self.get_option_undl(opt_code)
                if undl_code:
                    if undl_code in result:
                        result[undl_code].append(opt_code)
                    else:
                        result[undl_code] = [opt_code]
            return result

    def get_option_list(self,object,dedate,opttype = "",isavailavle = False):
        result = [];

        undlMarket = "";
        undlCode = "";
        marketcodeList = object.split('.');
        if(len(marketcodeList) !=2):
            return [];
        undlCode = marketcodeList[0]
        undlMarket = marketcodeList[1];
        market = ""
        if(undlMarket == "SH"):
            if undlCode == "000016" or undlCode == "000300" or undlCode == "000852" or undlCode == "000905":
                market = 'IF'
            else:
                market = "SHO"
        elif(undlMarket == "SZ"):
            market = "SZO";
        if(opttype.upper() == "C"):
            opttype = "CALL"
        elif(opttype.upper() == "P"):
            opttype = "PUT"
        optList = []
        if market == 'SHO':
            optList += get_stock_list_in_sector('上证期权')
            hisList = get_stock_list_in_sector('过期上证期权')
            if len(hisList) <= 0:
                hisList = self.get_his_contract_list(market)
            optList += hisList
        elif market == 'SZO':
            optList += get_stock_list_in_sector('深证期权')
            hisList = get_stock_list_in_sector('过期深证期权')
            if len(hisList) <= 0:
                hisList = self.get_his_contract_list(market)
            optList += hisList
        elif market == 'IF':
            optList += get_stock_list_in_sector('中金所')
            hisList = get_stock_list_in_sector('过期中金所')
            if len(hisList) <= 0:
                hisList = self.get_his_contract_list(market)
            optList += hisList
        for opt in optList:
            if(opt.find(market) < 0):
                continue
            inst = self.context.get_instrumentdetail(opt);
            if('ExtendInfo' not in inst):
                continue;
            if(opttype.upper()  != "" and  opttype.upper() != inst['ExtendInfo']["optType"]):
                continue;
            if( (len(dedate) == 6 and str(inst['ExpireDate']).find(dedate) < 0)  ):
                continue
            if( len(dedate) == 8): #option is trade,guosen demand
                createDate = inst['CreateDate'];
                openDate = inst['OpenDate'];
                if(createDate >= 1):
                    openDate = min(openDate,createDate);
                if(openDate < 20150101 or str(openDate) > dedate):
                    continue
                endDate = inst['ExpireDate'];
                if( isavailavle and  str(endDate) < dedate):
                    continue;
            if(inst['ProductID'].find(undlCode) > 0 or inst['ExtendInfo']['OptUndlCode'] == undlCode):
                result.append(opt);
        return result;


    def bsm_price(self,optType,targetPrice,strikePrice,riskFree,sigma,days,dividend = 0):
        optionType = "";
        if(optType.upper() == "C"):
            optionType = "CALL"
        if(optType.upper() == "P"):
            optionType = "PUT"
        if(type(targetPrice) == list):
            result = [];
            for price in targetPrice:
                bsmPrice= calc_bsm_price(optionType,strikePrice,float(price),riskFree,sigma,days,dividend)
                bsmPrice = round(bsmPrice,4)
                result.append(bsmPrice);
            return result;
        else:
            bsmPrice = calc_bsm_price(optionType,strikePrice,targetPrice,riskFree,sigma,days,dividend)
            result = round(bsmPrice,4)
            return result;

    def bsm_iv(self,optType,targetPrice,strikePrice,optionPrice,riskFree,days,dividend = 0):
        if(optType.upper() == "C"):
            optionType = "CALL"
        if(optType.upper() == "P"):
            optionType = "PUT"
        result = calc_bsm_iv(optionType,strikePrice,targetPrice,optionPrice,riskFree,days,dividend)
        result = round(result,4)
        return result

    def get_his_st_data(self,stockCode):
        #tradeDateList = ContextInfo.get_trading_dates(stockCode,'19900101','20380119',1,'1d')
        import json;
        data = get_st_status(stockCode);
        return data;

    def get_option_iv(self,opt_code):
        return  get_opt_iv(opt_code);

    def get_his_index_data(self,stockCode):
        data = get_history_index_weight(stockCode);
        return data
    @property
    def time_tick_size(self):
        return self.context.time_tick_size
    
    @property
    def current_bar(self):
        return self.context.current_bar
    
    @property
    def barpos(self):
        return self.context.barpos

    @property
    def benchmark(self):
        return self.context.benchmark

    @benchmark.setter
    def benchmark(self, value):
        self.context.benchmark = value
    
    @property
    def period(self):
        return self.context.period
    
    @property
    def capital(self):
        return self.context.capital

    @property
    def dividend_type(self):
        return self.context.dividend_type

    @capital.setter
    def capital(self, value):
        self.context.capital = value
    
    @property
    def refresh_rate(self):
        return self.context.refresh_rate

    @refresh_rate.setter
    def refresh_rate(self, value):
        self.context.refresh_rate = value
        
    @property
    def do_back_test(self):
        return self.context.do_back_test

    @do_back_test.setter
    def do_back_test(self, value):
        self.context.do_back_test = value
        
    @property
    def request_id(self):
        return self.context.request_id

        
    @property
    def stockcode(self):
        return self.context.stockcode
    @property
    def stockcode_in_rzrk(self):
        return self.context.stockcode_in_rzrk
    
    @property
    def market(self):
        return self.context.market
        
    @property
    def in_pythonworker(self):
        return self.context.in_pythonworker

    @property
    def start(self):
        return self.context.start
        
    @start.setter
    def start(self,value):
       self.context.start = value

    @property
    def end(self):
        return self.context.end
        
    @end.setter
    def end(self,value):
       self.context.end = value

    @property
    def data_info_level(self):
        return self.context.data_info_level
        
    @data_info_level.setter
    def data_info_level(self,value):
       self.context.data_info_level = value   

    def __deepcopy__(self, memo):
        #print "type:", type(self)
        new_obj = type(self)()
        # del last version when copy, only the last version is reverved
        # self.z8sglma_last_version = None
        for k, v in list(self.__dict__.items()):
            #print "k: %s v: %s" %(k, v)
            # contextInfo variable is from c++, not copy
            if k == "context":
                setattr(new_obj, k, v)
            elif k == "z8sglma_last_version":
                continue
            else:
                setattr(new_obj, k, copy.deepcopy(v, memo))
        return new_obj
        
    def get_factor_data(self, field_list, stock_list, start_date, end_date):
        import pandas as pd
        from collections import OrderedDict
        stocks = []
        if type(stock_list) == str:
            stocks.append(stock_list)
        else:
            stocks = stock_list
        pandasData = get_factor_datas(field_list, stocks, start_date, end_date)
        if not pandasData:
            return
        fields = pandasData['field']
        dates = pandasData['date']
        values = pandasData['value']
        
        if len(stocks) == 1 and len(dates) == 1:    #series
            series_list = []
            for value in values:
                if not value:
                    return
                for subValue in value:
                    series_list.append(subValue)
            return pd.Series(series_list, index = fields)
        elif len(stocks) == 1 and len(dates) > 1:   #index = dates, col = fields
            dataDict = OrderedDict()
            for n in range(len(values)):
                dataList = []
                if not values[n]:
                    return
                for subValue in values[n]:
                    dataList.append(subValue)
                dataDict[fields[n]] = pd.Series(dataList, index = dates)
            return pd.DataFrame(dataDict)
        elif len(stocks) > 1 and len(dates) == 1:   #index = stocks col = fields
            dataDict = OrderedDict()
            for n in range(len(values)):
                dataList = []
                if not values[n]:
                    return
                for subValue in values[n]:
                    dataList.append(subValue)
                dataDict[fields[n]] = pd.Series(dataList, index = stocks)
            return pd.DataFrame(dataDict)
        else:                                       #Key = stocks value = df(index = dates, col = fields)
            panels = OrderedDict()
            for i in range(len(stocks)):
                dataDict = OrderedDict()
                for j in range(len(values)):
                    dataList = []
                    value = values[j]
                    if not value:
                        return
                    for k in range(i * len(dates), (i + 1) * len(dates)):
                        dataList.append(value[k])
                    dataDict[fields[j]] = pd.Series(dataList, index = dates)
                panels[stocks[i]] = pd.DataFrame(dataDict)
            return panels
    
    def subscribe_quote(self, stock_code, period = 'follow', dividend_type = 'follow', result_type = '', callback = None):
        if callback:
            callback1 = callback
            if result_type.lower() == 'dict':
                def on_quote_wrapper(datas):
                    if datas.get('time', None):
                        callback1({stock_code : {k: v[-1] for k, v in datas.items()}})
                    return
                callback = on_quote_wrapper
            elif result_type.lower() == 'list':
                def on_quote_wrapper(datas):
                    callback1({stock_code : datas})
                    return
                callback = on_quote_wrapper
            else:
                import pandas as pd
                def on_quote_wrapper(datas):
                    datas2 = pd.DataFrame(datas)
                    datas2.index = datas2['stime']
                    callback1({stock_code : datas2})
                    return
                callback = on_quote_wrapper
        subID = self.context.subscribe_quote(stock_code, period, dividend_type, callback)
        if subID > 0:
            subInfo = {}
            subInfo['func'] = 'subscribe_quote'
            subInfo['stock_code'] = stock_code
            subInfo['stockCode'] = stock_code
            subInfo['period'] = period
            subInfo['dividend_type'] = dividend_type
            subInfo['dividendType'] = dividend_type
            self.subMap[subID] = subInfo
        return subID
        
    def subscribe_whole_quote(self, code_list, callback = None):
        if callback:
            callback1 = callback
            def on_quote_wrapper(datas):
                callback1(datas)
                return
            callback = on_quote_wrapper
        subID = self.context.subscribe_whole_quote(code_list, callback)
        if subID > 0:
            subInfo = {}
            subInfo['func'] = 'subscribe_whole_quote'
            subInfo['code_list'] = code_list
            self.subMap[subID] = subInfo
        return subID
        
    def unsubscribe_quote(self, subID):
        self.subMap.pop(subID, {})
        return self.context.unsubscribe_quote(subID)
        
    def get_all_subscription(self):
        return self.subMap

def timetag_to_datetime(timetag, format):
    import time
    timetag = timetag/1000
    time_local = time.localtime(timetag)
    return time.strftime(format,time_local)


def resume_context_info(context_info):
    last_barpos = context_info.z8sglma_last_barpos
    if context_info.barpos == last_barpos:
        for k, v in list(context_info.z8sglma_last_version.__dict__.items()):
            if k == "context":
                continue
            elif k == "z8sglma_last_version":
                continue
            else:
                setattr(context_info, k, copy.deepcopy(v))
    else:
        # print "not repeat, barpos:", args[0].barpos
        # print "curr bar: %i last bar: %i" % (args[0].barpos, context_info.last_barpos)
        context_info.z8sglma_last_barpos = context_info.barpos
        context_info.z8sglma_last_version = copy.deepcopy(context_info)

def request_general_file(strReq, callback):
    def wrapper(result, error_code, error_info):
        callback(result, error_code, error_info)
        return
    request_general_file_c(strReq, wrapper)
    