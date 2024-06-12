import tushare as ts
import json,datetime
import pandas as pd
import  pymysql
from dboprater import DB as db
configfile='./config/mysqlconfig.json'
class tradeday:
    def __init__(self):
        self.pro = ts.pro_api(db.get_config()['tushare'])

    #将交易日入库，1年执行一次即可
    def gettradeday(self):
        tradedaylist=[]
        try:
            alldays = self.pro.trade_cal()  # 得到所有日期，到今年年尾
            alldays=alldays.iloc[10000:,::]
            # alldays=pd.DataFrame(alldays.loc[:,'cal_date','is_open'])
            conn=db.dbconnect()
            currsor=conn.cursor(cursor=pymysql.cursors.DictCursor)
            sql ='insert into datelist (date,isopen) values(%s,%s)'
            for days in alldays.iterrows():
                date=days[1]['cal_date']
                is_open=days[1]['is_open']
                values=(date,is_open)
                currsor.execute(sql,values)
            conn.commit()
            currsor.close()
            conn.close()
        except BaseException as b:
            print(b)
    #判断当日是否为交易日
    @staticmethod
    def isTradeDay(*date1):
        '''date type:  2021-05-28'''
        len1=len(date1)
        if len1>0:
            date=str(date1[0])
        else:
            date = str(datetime.datetime.now().strftime('%Y-%m-%d'))
        flag=True
        conn = db.dbconnect()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        sql = 'select * from datelist where date=\''+date+'\''
        cursor.execute(sql)
        result=cursor.fetchall()
        if result:
            for data in result:
                isopen=data['isopen']
                if str(isopen)=='0':
                    flag=False
                    return flag
                else:
                    return flag
        else:
            print('取数据异常！')
    #获取最近一个交易日
    @staticmethod
    def getlastTradeday():
        conn = db.dbconnect()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        date=datetime.datetime.now().strftime('%Y-%m-%d')
        sql = 'select * from datelist where date<=\'' + date + '\''  #取到今天为止的所有日期数据
        cursor.execute(sql)
        result = cursor.fetchall()
        pddata=pd.DataFrame(result)
        if pddata.empty:
            return None
        else:
            pddata=pddata[pddata['isopen'] == 1] #留下全是交易日的数据
            res=pddata.iloc[-1, 0]
            return str(res)
    #获取上一个交易日
    @staticmethod
    def getyestodayTradeday(*date1):
        len1=len(date1)
        if len1>0:
            date=str(date1[0])
        else:
            date = str(datetime.datetime.now().strftime('%Y-%m-%d'))
        conn = db.dbconnect()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        sql = 'select * from datelist where date<=\'' + date + '\''  #取到今天为止的所有日期数据
        cursor.execute(sql)
        result = cursor.fetchall()
        pddata=pd.DataFrame(result)
        if pddata.empty:
            return None
        else:
            pddata=pddata[pddata['isopen'] == 1] #留下全是交易日的数据
            res=pddata.iloc[-2, 0]
            return str(res)
    #获取最近的第N个交易日
    @staticmethod
    def getlastNtradeday(n):
        '''n type int'''
        if str(n).isalpha():
            print('输入错误')
            return None
        conn = db.dbconnect()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        date = str(datetime.datetime.now().strftime('%Y-%m-%d'))
        sql = 'select * from datelist where date<=\'' + date + '\''  # 取到今天为止的所有日期数据
        cursor.execute(sql)
        result = cursor.fetchall()
        pddata = pd.DataFrame(result)
        if pddata.empty:
            return None
        else:
            pddata = pddata[pddata['isopen'] == 1]  # 留下全是交易日的数据
            res = pddata.iloc[-n, 0]
            return str(res)
    #获取前N个交易日列表
    @staticmethod
    def getlastNtradedaylist(n)   ->list:
        if str(n).isalpha():
            print('输入错误')
            return None
        conn = db.dbconnect()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        date = str(datetime.datetime.now().strftime('%Y-%m-%d'))
        sql = 'select * from datelist where date<=\'' + date + '\''  # 取到今天为止的所有日期数据
        cursor.execute(sql)
        result = cursor.fetchall()
        pddata = pd.DataFrame(result)
        if pddata.empty:
            return None
        else:
            pddata = pddata[pddata['isopen'] == 1]  # 留下全是交易日的数据
            pddata.reset_index(drop=True)
            # print(pddata.index)

            res = pddata.iloc[len(pddata)-n:len(pddata),0].values
            datelist=[]
            for date in res:
                date=date.strftime('%Y-%m-%d')
                # date=time.strftime('%Y-%m-%d',date)
                # print(date)
                datelist.append(str(date))
            return datelist

if __name__ == '__main__':
    test=tradeday()
    # isopen=test.isTradeDay('2021-05-29')
    # print(isopen)
    lasttradeday=test.getlastNtradedaylist(7)
    print(lasttradeday)
    # test.gettradeday()
'''
--南向资金数据
CREATE TABLE IF NOT EXISTS `datelist`(
date date,
isopen int
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
'''