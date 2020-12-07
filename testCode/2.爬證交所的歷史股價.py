# encoding=UTF-8
import datetime
import requests
import json
import time
import sqlite3
import CODE.config
conn = sqlite3.connect('C:/Users/user/Desktop/十大交易人/小胖下載加權指數報酬率Crawler/db/crawler.db')
c = conn.cursor()
startDate = CODE.config.startDate
twse_html_headers = CODE.config.twse_html_headers

for j in range(0,2000):
    time.sleep(5)
    daytime = datetime.datetime.strptime(startDate, "%Y-%m-%d") + datetime.timedelta(days=j)
    daytime = daytime.strftime("%Y-%m-%d %H:%M:%S").replace("-", "")[0:8];
    r = requests.get( "http://www.twse.com.tw/exchangeReport/MI_INDEX?response=json&date=" + daytime + "&type=ALLBUT0999", headers=twse_html_headers)
    d = json.loads(r.text)
    if json.dumps(d["stat"], ensure_ascii=False) == '"OK"':
        item_dict = json.loads(json.dumps(d["data5"]))
        #print "value=" , len(item_dict)
        for i in range(0, len(item_dict)):
           #print "i=" , i
           #print "leeeee=" , (json.dumps(d["data"][i][0], ensure_ascii=False)).replace("/", "")[4:8]
           close = (json.dumps(d["data5"][i][8], ensure_ascii=False))
           stock_id = (json.dumps(d["data5"][i][0], ensure_ascii=False))
           print ("stock_id,daytime,close=",stock_id,daytime,close)
           c.execute('UPDATE ThreeBigSUM SET close_price =' + close + ' WHERE stock_id =' + stock_id + ' and trade_date = ' + daytime + '')
           conn.commit()
print "Operation done successfully";
conn.close()
