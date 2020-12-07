# encoding=UTF-8
import datetime
import sqlite3
import requests
import json
import time
import CODE.config
from CODE.LineNotify import lineNotifyMessage

# 爬證交所滿足投信單日大買


def do_FIND_twse():
    conn1 = sqlite3.connect('C:/Users/user/Desktop/十大交易人/小胖下載加權指數報酬率Crawler/db/crawler.db')
    c1 = conn1.cursor()
    daytimeOne = time.strftime("%Y-%m-%d", time.localtime())
    daytimeTwo = daytimeOne.replace("-", "")[0:8];
    tempObject = "";
    cursor =  c1.execute("select *, funds_sum*close_price from ThreeBig where funds_sum*close_price > 200000000 and trade_date =" + daytimeTwo + " order by trade_date desc")
    for row in cursor:
        print("今天證交所第一題，股號:" + row[0] + "股名:" + row[1])
        lineNotifyMessage("今天證交所第一題，股號:" + row[0] + "股名:" + row[1] + "買超金額:" + str(int(row[11])*0.00000001) , 1)
        lineNotifyMessage("今天證交所第一題，股號:" + row[0] + "股名:" + row[1] + "買超金額:" + str(int(row[11])*0.00000001) , 2)
        lineNotifyMessage("今天證交所第一題，股號:" + row[0] + "股名:" + row[1] + "買超金額:" + str(int(row[11])*0.00000001) , 3)
        lineNotifyMessage("今天證交所第一題，股號:" + row[0] + "股名:" + row[1] + "買超金額:" + str(int(row[11])*0.00000001) , 4)
    cursor1 = c1.execute("select *, funds_sum * close_price from ThreeBig where funds_sum * close_price < -200000000 and trade_date =" + daytimeTwo + " order by trade_date desc")
    for row in cursor1:
        print("今天證交所反向第一題，股號:" + row[0] + "股名:" + row[1])
        lineNotifyMessage("今天證交所反向第一題，股號:" + row[0] + "股名:" + row[1] + "賣超金額:" + str(int(row[11])*0.00000001), 1)
        lineNotifyMessage("今天證交所反向第一題，股號:" + row[0] + "股名:" + row[1] + "賣超金額:" + str(int(row[11])*0.00000001), 2)
        lineNotifyMessage("今天證交所反向第一題，股號:" + row[0] + "股名:" + row[1] + "賣超金額:" + str(int(row[11])*0.00000001), 3)
        lineNotifyMessage("今天證交所反向第一題，股號:" + row[0] + "股名:" + row[1] + "賣超金額:" + str(int(row[11])*0.00000001), 4)
    cursor2 = c1.execute(' select * from ThreeBig where funds_sum*6.6 > volume and trade_date = ' + daytimeTwo)
    for row in cursor2:
        tempObject = tempObject + "(股號:" + str(row[0]).replace(" ","") + ";股名:" + str(row[1]).replace(" ","")  + ")        "
    if tempObject != "":
        print("今天證交所投信買超佔交易量超過15%，" + tempObject)
        lineNotifyMessage("今天證交所投信買超佔交易量超過15%，" + tempObject, 1)
        lineNotifyMessage("今天證交所投信買超佔交易量超過15%，" + tempObject, 3)
        lineNotifyMessage("今天證交所投信買超佔交易量超過15%，" + tempObject, 4)
    cursor3 = c1.execute(' select * from ThreeBig where funds_sum*5 < -1*volume and trade_date = ' + daytimeTwo)
    tempObject = "";
    for row in cursor3:
        tempObject = tempObject + "(股號:" + str(row[0]).replace(" ", "") + ";股名:" + str(row[1]).replace(" ","") + ")        "
    if tempObject != "":
        print("今天證交所投信賣超佔交易量超過20%，" + tempObject)
        lineNotifyMessage("今天證交所投信賣超佔交易量超過20%，" + tempObject, 1)
        lineNotifyMessage("今天證交所投信賣超佔交易量超過20%，" + tempObject, 3)
        lineNotifyMessage("今天證交所投信賣超佔交易量超過20%，" + tempObject, 4)
    conn1.commit()
    conn1.close()

# do_FIND_twse();