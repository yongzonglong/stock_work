# encoding=UTF-8
import datetime
import sqlite3
import requests
import json
import time

howManyMoneyBigThen = -500000000
beginDate = 20201015
endDate = 20201203
betweenDay = 20
conn1 = sqlite3.connect('C:/Users/user/Desktop/十大交易人/小胖下載加權指數報酬率Crawler/db/crawler.db')
conn2 = sqlite3.connect('C:/Users/user/Desktop/十大交易人/小胖下載加權指數報酬率Crawler/db/crawler.db')
c1 = conn1.cursor()
c2 = conn2.cursor()
cursor =  c1.execute("select stock_id from SecurityLendingSell group by stock_id order by stock_id DESC")

for row in cursor:
    # print "準備進入",row[0].replace(" ","");
    cursor2 = c2.execute('select *,cast((security_lending_back-security_lending_sell)*close_price AS int) from SecurityLendingSell  where stock_id = "' + row[0].replace(" ","") + '"')
    mylist = list()
    dateMyList = list()
    for row2 in cursor2:
        # print row2[0],row2[7];
        mylist.append(row2[6])
        dateMyList.append(row2[2])
    # print mylist
    # print dateMyList
    for i in range(0,mylist.__len__()-betweenDay):
        sum_money = 0
        for j in range(0,betweenDay):
            sum_money = sum_money + int(mylist[j+i] or 0)
        # print("sum_money=",sum_money);
        if(sum_money < howManyMoneyBigThen):
            if(dateMyList[i] > beginDate) & (dateMyList[i] <endDate):
                print("滿足條件",row2[0],row2[1],dateMyList[i],float(sum_money)/100000000)
conn1.commit()
conn1.close()


print("Operation done successfully");

