# encoding=UTF-8
import datetime
import sqlite3
import requests
import json
import time
import CODE.config

beginDate = "20200515"

def Find_Twse_Fund_Continue(beginDate):
    betweenDay = 20
    howManyMoneyBigThen = 400000000
    howManyMoneySmallThen = -400000000
    conn1 = sqlite3.connect('C:/Users/user/Desktop/十大交易人/小胖下載加權指數報酬率Crawler/db/crawler.db')
    conn2 = sqlite3.connect('C:/Users/user/Desktop/十大交易人/小胖下載加權指數報酬率Crawler/db/crawler.db')
    c1 = conn1.cursor()
    c2 = conn2.cursor()
    cursor =  c1.execute("select stock_id from ThreeBig group by stock_id order by stock_id DESC")
    target_buy_stock = "";
    target_sell_stock = "";
    for row in cursor:
        if beginDate ==0:
            cursor2 = c2.execute('select * from (select *, close_price * funds_sum from ThreeBig where stock_id = "' + row[0].replace(" ","") + '"' + 'order by trade_date desc limit 21) order by trade_date')
            daytimeOne = time.strftime("%Y-%m-%d", time.localtime())
            daytimeTwo = daytimeOne.replace("-", "")[0:8];
        else:
            cursor2 = c2.execute('select *,close_price*funds_sum from ThreeBig where stock_id = "' + row[0].replace(" ","") + '"')
            daytimeTwo = beginDate;
        mylist = list()
        dateMyList = list()
        for row2 in cursor2:
            mylist.append(row2[11])
            dateMyList.append(row2[2])
        for i in range(0,mylist.__len__()-betweenDay):
            sum_money = int(0)
            for j in range(0,betweenDay):
                # print("mylist[j+i]=",mylist[j+i])
                sum_money = sum_money + int(mylist[j+i])
            if(sum_money > howManyMoneyBigThen):
                if(dateMyList[i] >= int(beginDate)):
                    target_buy_stock = target_buy_stock + "("+ str(row2[0]) + str(row2[1]).replace(" ","") + str(dateMyList[i]) + ")         "
            if(sum_money < howManyMoneySmallThen):
                if(dateMyList[i] >= int(beginDate)):
                    target_sell_stock = target_sell_stock + "("+ str(row2[0]) + str(row2[1]).replace(" ","") + str(dateMyList[i]) + ")      "
    print("投信連買:" + target_buy_stock)
    print("投信連賣:" + target_sell_stock)
    conn1.commit()
    conn1.close()


# Find_Twse_Fund_Continue(0)

Find_Twse_Fund_Continue(beginDate)