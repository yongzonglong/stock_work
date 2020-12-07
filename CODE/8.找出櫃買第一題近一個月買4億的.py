# encoding=UTF-8
import datetime
import sqlite3
import requests
import json
import time
import CODE.config

howManyMoneyBigThen = 400000000
howManyMoneySmallThen = -400000000

beginDate = 20200515
betweenDay = 20

conn1 = sqlite3.connect('C:/Users/user/Desktop/十大交易人/小胖下載加權指數報酬率Crawler/db/crawler.db')
conn2 = sqlite3.connect('C:/Users/user/Desktop/十大交易人/小胖下載加權指數報酬率Crawler/db/crawler.db')
c1 = conn1.cursor()
c2 = conn2.cursor()
cursor =  c1.execute("select stock_id from ThreeBigOTC group by stock_id order by stock_id DESC")
target_buy_stock = "";
target_sell_stock = "";
for row in cursor:
    # print "準備進入",row[0].replace(" ","");
    cursor2 = c2.execute('select *,close_price*funds_sum from ThreeBigOTC where stock_id = "' + row[0].replace(" ","") + '"')
    mylist = list()
    dateMyList = list()
    for row2 in cursor2:
        # print row2[0],row2[7];
        mylist.append(row2[11])
        dateMyList.append(row2[2])
    # print mylist
    # print dateMyList
    for i in range(0,mylist.__len__()-betweenDay):
        sum_money = 0
        for j in range(0,betweenDay):
            # print row2[0],mylist[j+i]
            if(mylist[j+i] == None):
                mylist[j + i] = 0
            sum_money = sum_money + mylist[j+i]
        # print("sum_money=",sum_money);
        if(sum_money > howManyMoneyBigThen):
            if(dateMyList[i] > beginDate):
                print("滿足條件買超",row2[0],row2[1],dateMyList[i])
                target_buy_stock = target_buy_stock + "(" + str(row2[0]) + str(row2[1]).replace(" ", "") + str(
                    dateMyList[i]) + ")         "
        if(sum_money < howManyMoneySmallThen):
            if(dateMyList[i] > beginDate):
                print("滿足條件賣超",row2[0],row2[1],dateMyList[i])
                target_sell_stock = target_sell_stock + "(" + str(row2[0]) + str(row2[1]).replace(" ", "") + str(
                    dateMyList[i]) + ")      "
print("投信連買:" + target_buy_stock)
print("投信連賣:" + target_sell_stock)
conn1.commit()
conn1.close()


print("Operation done successfully");

