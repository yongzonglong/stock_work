# encoding=UTF-8
import requests
import json
import sqlite3
from bs4 import BeautifulSoup

r = requests.get("http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=20190225&stockNo=2330&_=1551104808314") #

trade_date = "20180213"
trade_date = trade_date[4:8]
d = json.loads(r.text)
for i in range(0,(json.dumps(d["data"], ensure_ascii=False).__len__())-1):
    print (json.dumps(d["data"][i][0], ensure_ascii=False)).replace("/", "")[4:8]
    print "trade_date=" + trade_date
    if trade_date == (json.dumps(d["data"][i][0], ensure_ascii=False)).replace("/", "")[4:8]:
        close = (json.dumps(d["data"][i][6], ensure_ascii=False))
        print "第" , i , "筆"
        print "close=" + close