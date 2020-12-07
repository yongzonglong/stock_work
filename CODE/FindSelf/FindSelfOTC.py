# encoding=UTF-8
import datetime
import sqlite3
import requests
import json
import time
import CODE.config
from CODE.LineNotify import lineNotifyMessage


# 爬櫃買中心滿足自營商單日大買


def do_SELF_otc():
    conn1 = sqlite3.connect('C:/Users/user/Desktop/十大交易人/小胖下載加權指數報酬率Crawler/db/crawler.db')
    c1 = conn1.cursor()
    daytimeOne = time.strftime("%Y-%m-%d", time.localtime())
    daytimeTwo = daytimeOne.replace("-", "")[0:8];
    # daytimeTwo = "20200114"
    # print(daytimeTwo);
    cursor =  c1.execute("select *, selfEmployed_sum*close_price from ThreeBigOTC where selfEmployed_sum*close_price > 100000000 and trade_date =" + daytimeTwo + " order by trade_date desc")
    for row in cursor:
        print("今天櫃買中心自營商單日爆買，股號:" + row[0] + "股名:" + row[1])
        # lineNotifyMessage("今天櫃買中心自營商單日爆買，股號:" + row[0] + "股名:" + row[1], 1)
        # lineNotifyMessage("今天櫃買中心自營商單日爆買，股號:" + row[0] + "股名:" + row[1], 3)

    cursor =  c1.execute("select *, selfEmployed_sum*close_price from ThreeBigOTC where selfEmployed_sum*close_price < -100000000 and trade_date =" + daytimeTwo + " order by trade_date desc")
    for row in cursor:
        print("今天櫃買中心自營商單日爆賣，股號:" + row[0] + "股名:" + row[1])
        # lineNotifyMessage("今天櫃買中心自營商單日爆賣，股號:" + row[0] + "股名:" + row[1], 1)
        # lineNotifyMessage("今天櫃買中心自營商單日爆賣，股號:" + row[0] + "股名:" + row[1], 3)
    conn1.commit()
    conn1.close()

# do_SELF_otc();