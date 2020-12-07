# encoding=UTF-8
import requests
from bs4 import BeautifulSoup
r = requests.get("http://www.twse.com.tw/fund/T86?response=json&date=20190221&selectType=ALLBUT0999&_=1550649901796") #
import json
import sqlite3
conn = sqlite3.connect('C:/Users/user/Desktop/十大交易人/小胖下載加權指數報酬率Crawler/db/crawler.db')
d = json.loads(r.text)
c = conn.cursor()
for i in range(0,(json.dumps(d["data"][0], ensure_ascii=False).__len__())-1):
    stock_id = (json.dumps(d["data"][i][0], ensure_ascii=False))
    name = (json.dumps(d["data"][i][1], ensure_ascii=False))
    trade_date = (json.dumps(d["date"], ensure_ascii=False))
    funds_buy = (json.dumps(d["data"][i][8], ensure_ascii=False))
    funds_sell = (json.dumps(d["data"][i][9], ensure_ascii=False))
    funds_sum = (json.dumps(d["data"][i][10], ensure_ascii=False))
    c.execute("INSERT INTO ThreeBigSUM (stock_id,name,trade_date,funds_buy,funds_sell,funds_sum) VALUES (" + stock_id + "," + name + "," + trade_date + "," + funds_buy +"," + funds_sell +"," + funds_sum + ")")
conn.commit()
print "Records created successfully";
conn.close()
print (json.dumps(d["data"][0], ensure_ascii=False).__len__())