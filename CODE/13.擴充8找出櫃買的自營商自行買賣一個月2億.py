# encoding=UTF-8
import datetime
import sqlite3
import requests
import json
import time
import CODE.config
startDate = CODE.config.startDate
howManyMoneyBigThen = 200000000
beginDate = 20150000
betweenDay = 20


conn1 = sqlite3.connect('C:/Users/user/Desktop/十大交易人/小胖下載加權指數報酬率Crawler/db/crawler.db')
conn2 = sqlite3.connect('C:/Users/user/Desktop/十大交易人/小胖下載加權指數報酬率Crawler/db/crawler.db')
c1 = conn1.cursor()
c2 = conn2.cursor()
cursor =  c1.execute("select stock_id from ThreeBigOTC group by stock_id order by stock_id DESC")

for row in cursor:
    # print "準備進入",row[0].replace(" ","");
    cursor2 = c2.execute('select *,close_price*selfEmployed_sum from ThreeBigOTC where stock_id = "' + row[0].replace(" ","") + '"')
    mylist = list()
    dateMyList = list()
    for row2 in cursor2:
        # print row2[0],row2[7];
        mylist.append(row2[10]) # 跟投信差別只有改這個
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
        if(sum_money > howManyMoneyBigThen):  # 跟投信差別只有改這個
            if(dateMyList[i] > beginDate):
                print("滿足條件",row2[0],row2[1],dateMyList[i])
conn1.commit()
conn1.close()



