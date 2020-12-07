# encoding=UTF-8
import datetime
import sqlite3
import math
import requests
import json
import time
from CODE.LineNotify import lineNotifyMessage

startDate = 20170101

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
    cursor =  c1.execute("select * from AllFutures")
    lastlist = list()
    for row in cursor:
        if len(lastlist) == 0:
            lastlist = row
        else:
            if row[1] >= int(beginDate):
                print("今天和上一個交易日外資期貨多單數相差" + str(row[14] -lastlist[14]) + ";收盤價相差" + str( math.floor(float(row[2].replace(",",""))) - math.floor(float(lastlist[2].replace(",","")))) )
                lineNotifyMessage("今天和上一個交易日外資期貨多單數相差" + str(row[14] -lastlist[14]) + ";收盤價相差" + str( math.floor(float(row[2].replace(",",""))) - math.floor(float(lastlist[2].replace(",","")))), 1)
                lineNotifyMessage("今天和上一個交易日外資期貨多單數相差" + str(row[14] -lastlist[14]) + ";收盤價相差" + str( math.floor(float(row[2].replace(",",""))) - math.floor(float(lastlist[2].replace(",","")))), 3)
                lineNotifyMessage("今天和上一個交易日外資期貨多單數相差" + str(row[14] -lastlist[14]) + ";收盤價相差" + str( math.floor(float(row[2].replace(",",""))) - math.floor(float(lastlist[2].replace(",","")))), 4)
            if (lastlist[14] -row[14])>4000:
                if ( math.floor(float(lastlist[2].replace(",",""))) -math.floor(float(row[2].replace(",",""))) ) < -40:
                    if row[1] >= int(beginDate):
                        print("外資期貨做空還大漲條件成立" + str(row[1]) + "，昨日期貨多單數:" + str(lastlist[14]) + "，今日期貨多單數:" + str(row[14]) )
                        lineNotifyMessage("外資期貨做空還大漲條件成立" + str(row[1]) + "，昨日期貨多單數:" + str(lastlist[14]) + "，今日期貨多單數:" + str(row[14]), 1)
                        lineNotifyMessage("外資期貨做空還大漲條件成立" + str(row[1]) + "，昨日期貨多單數:" + str(lastlist[14]) + "，今日期貨多單數:" + str(row[14]), 3)
                        lineNotifyMessage("外資期貨做空還大漲條件成立" + str(row[1]) + "，昨日期貨多單數:" + str(lastlist[14]) + "，今日期貨多單數:" + str(row[14]), 4)
            if (lastlist[14] - row[14]) < -4000:
                if ( math.floor(float(lastlist[2].replace(",",""))) -math.floor(float(row[2].replace(",",""))) ) > 40:
                    if row[1] >= int(beginDate):
                        print("外資期貨做多還大跌條件成立" + str(row[1]) + "，昨日期貨多單數:" + str(lastlist[14]) + "，今日期貨多單數:" + str(row[14]) )
                        lineNotifyMessage("外資期貨做多還大跌條件成立" + str(row[1]) + "，昨日期貨多單數:" + str(lastlist[14]) + "，今日期貨多單數:" + str(row[14]), 1)
                        lineNotifyMessage("外資期貨做多還大跌條件成立" + str(row[1]) + "，昨日期貨多單數:" + str(lastlist[14]) + "，今日期貨多單數:" + str(row[14]), 3)
                        lineNotifyMessage("外資期貨做多還大跌條件成立" + str(row[1]) + "，昨日期貨多單數:" + str(lastlist[14]) + "，今日期貨多單數:" + str(row[14]), 4)


            # if ((lastlist[14] -row[14])/lastlist[14]) > 0.05:
            #     if ( math.floor(float(lastlist[2].replace(",",""))) -math.floor(float(row[2].replace(",",""))) ) < -40:
            #         print("做空還大漲",+ row[1])
            # if ((lastlist[14] - row[14])/lastlist[14]) < -0.05:
            #     if ( math.floor(float(lastlist[2].replace(",",""))) -math.floor(float(row[2].replace(",",""))) ) > 40:
            #         print("做多還大跌",+ row[1])


            # 特定法人廢到笑
            # print(  (lastlist[9]- lastlist[10]) - (row[9] - row[10])  )
            # if ( (lastlist[9]- lastlist[10]) - (row[9] - row[10]) )> 5000:
            #     if ( math.floor(float(lastlist[2].replace(",",""))) -math.floor(float(row[2].replace(",",""))) ) < -40:
            #         if row[1] >= int(beginDate):
            #             if (lastlist[9] > row[9]) and (lastlist[10] < row[10]):
            #                 print("特定十大做空還大漲條件成立" + str(row[1]) + "，昨日期貨多單數:" + str(lastlist[14]) + "，今日期貨多單數:" + str(row[14]) )
            # if ((lastlist[9]- lastlist[10]) - (row[9] - row[10])) < -5000:
            #     if ( math.floor(float(lastlist[2].replace(",",""))) -math.floor(float(row[2].replace(",",""))) ) > 40:
            #         if row[1] >= int(beginDate):
            #             if (lastlist[9] < row[9]) and (lastlist[10] > row[10]):
            #                 print("特定十大做多還大跌條件成立" + str(row[1]) + "，昨日期貨多單數:" + str(lastlist[14]) + "，今日期貨多單數:" + str(row[14]))



            if ( (lastlist[5]- lastlist[6]) - (row[5] - row[6]) )> 4000:
                if ( math.floor(float(lastlist[2].replace(",",""))) -math.floor(float(row[2].replace(",",""))) ) < -40:
                    if row[1] >= int(beginDate):
                        if (lastlist[5] > row[5]) and (lastlist[6] < row[6]):
                            print("非特定十大做空還大漲條件成立" + str(row[1]) + "，昨日期貨多單數:" + str(lastlist[14]) + "，今日期貨多單數:" + str(row[14]) )
                            lineNotifyMessage("非特定十大做空還大漲條件成立" + str(row[1]) + "，昨日期貨多單數:" + str(lastlist[14]) + "，今日期貨多單數:" + str(row[14]) , 1)
                            lineNotifyMessage("非特定十大做空還大漲條件成立" + str(row[1]) + "，昨日期貨多單數:" + str(lastlist[14]) + "，今日期貨多單數:" + str(row[14]) , 3)
                            lineNotifyMessage("非特定十大做空還大漲條件成立" + str(row[1]) + "，昨日期貨多單數:" + str(lastlist[14]) + "，今日期貨多單數:" + str(row[14]) , 4)
            if ((lastlist[5]- lastlist[6]) - (row[5] - row[6])) < -4000:
                if ( math.floor(float(lastlist[2].replace(",",""))) -math.floor(float(row[2].replace(",",""))) ) > 40:
                    if row[1] >= int(beginDate):
                        if (lastlist[5] < row[5]) and (lastlist[6] > row[6]):
                            print("非特定十大做多還大跌條件成立" + str(row[1]) + "，昨日期貨多單數:" + str(lastlist[14]) + "，今日期貨多單數:" + str(row[14]))
                            lineNotifyMessage("非特定十大做多還大跌條件成立" + str(row[1]) + "，昨日期貨多單數:" + str(lastlist[14]) + "，今日期貨多單數:" + str(row[14]), 1)
                            lineNotifyMessage("非特定十大做多還大跌條件成立" + str(row[1]) + "，昨日期貨多單數:" + str(lastlist[14]) + "，今日期貨多單數:" + str(row[14]), 3)
                            lineNotifyMessage("非特定十大做多還大跌條件成立" + str(row[1]) + "，昨日期貨多單數:" + str(lastlist[14]) + "，今日期貨多單數:" + str(row[14]), 4)
            if ( (lastlist[3]- lastlist[4]) - (row[3] - row[4]) )> 4000:
                if ( math.floor(float(lastlist[2].replace(",",""))) -math.floor(float(row[2].replace(",",""))) ) < -40:
                    if row[1] >= int(beginDate):
                        if (lastlist[3] > row[3]) and (lastlist[4] < row[4]):
                            print("非特定五大做空還大漲條件成立" + str(row[1]) + "，昨日期貨多單數:" + str(lastlist[14]) + "，今日期貨多單數:" + str(row[14]) )
                            lineNotifyMessage("非特定五大做空還大漲條件成立" + str(row[1]) + "，昨日期貨多單數:" + str(lastlist[14]) + "，今日期貨多單數:" + str(row[14]), 1)
                            lineNotifyMessage("非特定五大做空還大漲條件成立" + str(row[1]) + "，昨日期貨多單數:" + str(lastlist[14]) + "，今日期貨多單數:" + str(row[14]), 3)
                            lineNotifyMessage("非特定五大做空還大漲條件成立" + str(row[1]) + "，昨日期貨多單數:" + str(lastlist[14]) + "，今日期貨多單數:" + str(row[14]), 4)
            if ((lastlist[3]- lastlist[4]) - (row[3] - row[4])) < -4000:
                if ( math.floor(float(lastlist[2].replace(",",""))) -math.floor(float(row[2].replace(",",""))) ) > 40:
                    if row[1] >= int(beginDate):
                        if (lastlist[3] < row[3]) and (lastlist[4] > row[4]):
                            print("非特定五大做多還大跌條件成立" + str(row[1]) + "，昨日期貨多單數:" + str(lastlist[14]) + "，今日期貨多單數:" + str(row[14]))
                            lineNotifyMessage("非特定五大做多還大跌條件成立" + str(row[1]) + "，昨日期貨多單數:" + str(lastlist[14]) + "，今日期貨多單數:" + str(row[14]), 1)
                            lineNotifyMessage("非特定五大做多還大跌條件成立" + str(row[1]) + "，昨日期貨多單數:" + str(lastlist[14]) + "，今日期貨多單數:" + str(row[14]), 3)
                            lineNotifyMessage("非特定五大做多還大跌條件成立" + str(row[1]) + "，昨日期貨多單數:" + str(lastlist[14]) + "，今日期貨多單數:" + str(row[14]), 4)
            lastlist = row
    conn1.close()
    conn2.close()

# Find_AllFurtrues("20201027")
