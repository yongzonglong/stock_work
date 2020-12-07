# encoding=UTF-8
import datetime
import sqlite3
import requests
import json
import time
print '開始爬蟲'
import CODE.config
startDate = CODE.config.startDate
for j in range(0,2000):
    #time.sleep(3)
    conn1 = sqlite3.connect('C:/Users/user/Desktop/十大交易人/小胖下載加權指數報酬率Crawler/db/crawler.db')
    c1 = conn1.cursor()
    daytime = datetime.datetime.strptime(startDate, "%Y-%m-%d") + datetime.timedelta(days=j)
    daytime = daytime.strftime("%Y-%m-%d %H:%M:%S").replace("-", "")[0:8];
    chinedaytime = str(int(daytime[0:4])-1911) + "/" + daytime[4:6] + "/" + daytime[6:8]
    print "chinedaytime=" , chinedaytime
    r = requests.get("http://www.tpex.org.tw/web/stock/3insti/daily_trade/3itrade_hedge_result.php?l=zh-tw&se=EW&t=D&d=" + chinedaytime + "&_=1551422327244")
    d = json.loads(r.text)
    global k
    k = 5  # K來設定20171215前後資料格式不同
    print json.dumps(d["reportTitle"])
    if json.dumps(d["reportTitle"]) != '""':
        item_dict = json.loads((json.dumps(d["aaData"][0], ensure_ascii=False)))
        if len(item_dict) == 25:
            k = 11
        item_dict2 = json.loads((json.dumps(d["aaData"], ensure_ascii=False)))
        for i in range(0, len(item_dict2)):
            stock_id = (json.dumps(d["aaData"][i][0], ensure_ascii=False))
            name = (json.dumps(d["aaData"][i][1], ensure_ascii=False))
            trade_date = daytime
            funds_buy = (json.dumps(d["aaData"][i][int(k)], ensure_ascii=False)).replace(",", "")
            funds_sell = (json.dumps(d["aaData"][i][int(k)+1], ensure_ascii=False)).replace(",", "")
            funds_sum = (json.dumps(d["aaData"][i][int(k)+2], ensure_ascii=False)).replace(",", "")
            print "(stock_id,name,trade_date,funds_buy,funds_sell,funds_sum)" , stock_id,name,trade_date,funds_buy,funds_sell,funds_sum
            c1.execute( "INSERT INTO ThreeBigOtcSUM (stock_id,name,trade_date,funds_buy,funds_sell,funds_sum) VALUES (" + stock_id + "," + name + "," + trade_date + "," + funds_buy + "," + funds_sell + "," + funds_sum + ")")
            conn1.commit()
        print daytime + "成功下載";
    else:
        print daytime + "沒有下載到";
    conn1.close()
print "Operation done successfully";

