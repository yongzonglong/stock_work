# encoding=UTF-8
import datetime
import sqlite3
import requests
import json
import time
import CODE.config

print '開始爬蟲'
startDate = CODE.config.startDate
for j in range(0,999):
    time.sleep(5)
    conn1 = sqlite3.connect('C:/Users/user/Desktop/十大交易人/小胖下載加權指數報酬率Crawler/db/crawler.db')
    c1 = conn1.cursor()
    daytime = datetime.datetime.strptime(startDate, "%Y-%m-%d") + datetime.timedelta(days=j)
    daytime = daytime.strftime("%Y-%m-%d %H:%M:%S").replace("-", "")[0:8];
    r = requests.get("http://www.twse.com.tw/fund/T86?response=json&date=" + daytime + "&selectType=ALLBUT0999&_=1550649901796")
    d = json.loads(r.text)
    global k
    k = 5  # K來設定20171215前後資料格式不同
    if  json.dumps(d["stat"], ensure_ascii=False) == '"OK"':
        if len(json.dumps(d["fields"])) == 1156:
            k = 8
    print json.dumps(d["stat"], ensure_ascii=False)
    if json.dumps(d["stat"], ensure_ascii=False) == '"OK"':
        item_dict = json.loads((json.dumps(d["data"], ensure_ascii=False)))
        for i in range(0, len(item_dict)):
            stock_id = (json.dumps(d["data"][i][0], ensure_ascii=False))
            name = (json.dumps(d["data"][i][1], ensure_ascii=False))
            trade_date = (json.dumps(d["date"], ensure_ascii=False))
            funds_buy = (json.dumps(d["data"][i][int(k)], ensure_ascii=False)).replace(",", "")
            funds_sell = (json.dumps(d["data"][i][int(k)+1], ensure_ascii=False)).replace(",", "")
            funds_sum = (json.dumps(d["data"][i][int(k)+2], ensure_ascii=False)).replace(",", "")
            c1.execute( "INSERT INTO ThreeBigSUM (stock_id,name,trade_date,funds_buy,funds_sell,funds_sum) VALUES (" + stock_id + "," + name + "," + trade_date + "," + funds_buy + "," + funds_sell + "," + funds_sum + ")")
            conn1.commit()
        print daytime + "成功下載";
    elif json.dumps(d["stat"], ensure_ascii=False) == '"查詢日期大於可查詢最大日期，請重新查詢!"':
        break
    else:
        print daytime + "沒有下載到";
    conn1.close()
print "Operation done successfully";

