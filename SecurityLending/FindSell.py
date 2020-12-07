# encoding=UTF-8
import datetime
import sqlite3
import requests
import json
import time
import SecurityLending.config
from CODE.LineNotify import lineNotifyMessage
beginDate = SecurityLending.config.startDate
beginDate = beginDate.replace("-", "")[0:8];


# beginDate = 20191100
# 爬證交所借券賣出

def find_sell(daytime):
    if daytime == 0:
        daytimeOne = time.strftime("%Y-%m-%d", time.localtime())
        daytimeTwo = daytimeOne.replace("-", "")[0:8];
        daytime = daytimeTwo
    conn1 = sqlite3.connect('C:/Users/user/Desktop/十大交易人/小胖下載加權指數報酬率Crawler/db/crawler.db')
    c1 = conn1.cursor()
    tempObject = "";
    cursor =  c1.execute("select *,security_lending_sell*close_price from SecurityLendingSell where security_lending_sell*close_price>200000000")

    for row in cursor:
        if (row[2] >= int(daytime) ) :
        # if (row[2] > beginDate) and (row[0] != '2330' and row[0] != '2317' and row[0] != '2454' and row[0] != '2882' and row[0] != '00637L' and row[0] != '2412'):
            tempObject = tempObject + "(股號:" + str(row[0]) + "股名:" + str(row[1]) + "日期:" + str(row[2]) + "收盤價:" + str(row[5]) + ")      "
    if tempObject != "":
        print("滿足條件借券賣出", tempObject)
        lineNotifyMessage("今天借券賣出，" + tempObject, 1)
        lineNotifyMessage("今天借券賣出，" + tempObject, 3)
    # print("滿足條件借券賣出",row[0],row[1],row[2],row[5])
    # lineNotifyMessage("今天借券賣出，股號:" + str(row[0]) + "股名:" + str(row[1]) + "日期:" + str(row[2]) + "收盤價:" + str(row[5]), 1)
    # lineNotifyMessage("今天借券賣出，股號:" + str(row[0]) + "股名:" + str(row[1]) + "日期:" + str(row[2]) + "收盤價:" + str(row[5]), 3)
    conn1.commit()
    conn1.close()


# find_sell(0)