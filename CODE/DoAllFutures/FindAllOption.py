# encoding=UTF-8
import datetime
import sqlite3
import math
import requests
import json
import time
from CODE.LineNotify import lineNotifyMessage

# 找出選擇權何時可以進場，但是似乎外資拿選擇權避險拿期貨賺錢

startDate = 20180123

def Find_AllFurtrues(beginDate):
    if beginDate == 0:
        daytimeOne = time.strftime("%Y-%m-%d", time.localtime())
        daytimeTwo = daytimeOne.replace("-", "")[0:8];
        beginDate = daytimeTwo
        # print(beginDate);
    conn1 = sqlite3.connect('C:/Users/user/Desktop/十大交易人/小胖下載加權指數報酬率Crawler/db/crawler.db')
    conn2 = sqlite3.connect('C:/Users/user/Desktop/十大交易人/小胖下載加權指數報酬率Crawler/db/crawler.db')
    c1 = conn1.cursor()
    c2 = conn2.cursor()
    cursor =  c1.execute("select * from AllFutures where trade_date >=" + str(beginDate) )
    lastlist = list()
    for row in cursor:
        if len(lastlist) == 0:
            lastlist = row
        else:
            # if row[1] >= int(beginDate):
                # print("今天和上一個交易日外資期貨多單數相差" + str(row[25] -lastlist[25]) + ";收盤價相差" + str( math.floor(float(row[2].replace(",",""))) - math.floor(float(lastlist[2].replace(",","")))) )
                # lineNotifyMessage("今天和上一個交易日外資期貨多單數相差" + str(row[14] -lastlist[14]) + ";收盤價相差" + str( math.floor(float(row[2].replace(",",""))) - math.floor(float(lastlist[2].replace(",","")))), 1)
                # lineNotifyMessage("今天和上一個交易日外資期貨多單數相差" + str(row[14] -lastlist[14]) + ";收盤價相差" + str( math.floor(float(row[2].replace(",",""))) - math.floor(float(lastlist[2].replace(",","")))), 3)
            if (lastlist[25] -row[25])>5000 and (lastlist[28] -row[28]) < 0 and(lastlist[14] -row[14])>= 0 :
                if ( math.floor(float(lastlist[2].replace(",",""))) -math.floor(float(row[2].replace(",",""))) ) < -40:
                    if row[1] >= int(beginDate):
                        print("外資選擇權做空還大漲條件成立" + str(row[1]) + "，昨日買權多單數:" + str(lastlist[25]) + "，今日買權多單數:" + str(row[25]) )
                        # lineNotifyMessage("外資期貨做空還大漲條件成立" + str(row[1]) + "，昨日期貨多單數:" + str(lastlist[14]) + "，今日期貨多單數:" + str(row[14]), 1)
                        # lineNotifyMessage("外資期貨做空還大漲條件成立" + str(row[1]) + "，昨日期貨多單數:" + str(lastlist[14]) + "，今日期貨多單數:" + str(row[14]), 3)
            if (lastlist[25] - row[25]) < -5000 and (lastlist[28] -row[28]) > 0 and(lastlist[14] -row[14])<= 0:
                if ( math.floor(float(lastlist[2].replace(",",""))) -math.floor(float(row[2].replace(",",""))) ) > 40:
                    if row[1] >= int(beginDate):
                        print("外資選擇權做多還大跌條件成立" + str(row[1]) + "，昨日買權多單數:" + str(lastlist[25]) + "，今日買權多單數:" + str(row[25]) )
                        # lineNotifyMessage("外資期貨做多還大跌條件成立" + str(row[1]) + "，昨日期貨多單數:" + str(lastlist[14]) + "，今日期貨多單數:" + str(row[14]), 1)
                        # lineNotifyMessage("外資期貨做多還大跌條件成立" + str(row[1]) + "，昨日期貨多單數:" + str(lastlist[14]) + "，今日期貨多單數:" + str(row[14]), 3)
            lastlist = row
    conn1.close()
    conn2.close()


# Find_AllFurtrues("20200220")