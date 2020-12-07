# encoding=UTF-8
import sqlite3
import requests
import json
conn1 = sqlite3.connect('C:/Users/user/Desktop/十大交易人/小胖下載加權指數報酬率Crawler/db/crawler.db')
c1 = conn1.cursor()
print("Opened database successfully");
cursor = c1.execute("select * from CrawlerDate where crawler_type='TX'")
for row in cursor:
   print("trade_date= ", row[1].replace("-", ""))
   print("status= ", row[2])
   if row[2]  == 1:
       r = requests.get("http://www.twse.com.tw/fund/T86?response=json&date=" + row[1].replace("-", "") + "&selectType=ALLBUT0999&_=1550649901796")
       d = json.loads(r.text)
       conn2 = sqlite3.connect('C:/Users/user/Desktop/十大交易人/小胖下載加權指數報酬率Crawler/db/crawler.db')
       c2 = conn2.cursor()
       for i in range(0, (json.dumps(d["data"][0], ensure_ascii=False).__len__()) - 1):
           stock_id = (json.dumps(d["data"][i][0], ensure_ascii=False))
           name = (json.dumps(d["data"][i][1], ensure_ascii=False))
           trade_date = (json.dumps(d["date"], ensure_ascii=False))
           funds_buy = (json.dumps(d["data"][i][8], ensure_ascii=False))
           funds_sell = (json.dumps(d["data"][i][9], ensure_ascii=False))
           funds_sum = (json.dumps(d["data"][i][10], ensure_ascii=False))
           c2.execute("INSERT INTO ThreeBigSUM (stock_id,name,trade_date,funds_buy,funds_sell,funds_sum) VALUES (" + stock_id + "," + name + "," + trade_date + "," + funds_buy + "," + funds_sell + "," + funds_sum + ")")
       conn2.commit()
       print("Records created successfully")
       conn2.close()
print("Operation done successfully")
conn1.close()