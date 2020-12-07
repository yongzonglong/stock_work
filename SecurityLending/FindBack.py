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


money = "200000000"
# beginDate = 20191200

# 爬證交所借券回補


def find_back(daytime):
    if daytime == 0:
        daytimeOne = time.strftime("%Y-%m-%d", time.localtime())
        daytimeTwo = daytimeOne.replace("-", "")[0:8];
        daytime = daytimeTwo
    conn1 = sqlite3.connect('C:/Users/user/Desktop/十大交易人/小胖下載加權指數報酬率Crawler/db/crawler.db')
    c1 = conn1.cursor()
    tempObject = "";
    cursor =  c1.execute("select *,security_lending_back*close_price from SecurityLendingSell where security_lending_back*close_price>" + money)
    for row in cursor:
        if (row[2] >= int(daytime) ):
        # if (row[2] > beginDate) and (row[0] != '2330' and row[0] != '2317' and row[0] != '2454' and row[0] != '2882' and row[0] != '00637L' and row[0] != '2412' and row[0] != '2412'):
            tempObject = tempObject + "(股號:" + str(row[0]) + "股名:" + str(row[1]) + "日期:" + str(row[2]) + "收盤價:" + str(row[5]) + ")      "
    if tempObject != "":
        print("滿足條件借券回補", tempObject)
        lineNotifyMessage("今天借券回補，" + tempObject, 1)
        lineNotifyMessage("今天借券回補，" + tempObject, 3)
    conn1.commit()
    conn1.close()

# find_back(0)


