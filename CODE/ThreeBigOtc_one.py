# encoding=UTF-8
import datetime
import sqlite3
import requests
import json
import time
import CODE.config

startDate = CODE.config.startDate


# 爬櫃買中心的三大法人



def do_big_twse_three_big_OTC(tempstartDate,index):
    for j in range(0,index):
        time.sleep(2)
        conn1 = sqlite3.connect('C:/Users/user/Desktop/十大交易人/小胖下載加權指數報酬率Crawler/db/crawler.db')
        c1 = conn1.cursor()
        if tempstartDate == 0:
            daytimeOne = time.strftime("%Y-%m-%d", time.localtime())
            daytimeTwo = daytimeOne.replace("-", "")[0:8];
            daytime = daytimeTwo
            chinedaytime = str(int(daytimeTwo[0:4]) - 1911) + "/" + daytimeTwo[4:6] + "/" + daytimeTwo[6:8]
        else:
            daytime = datetime.datetime.strptime(tempstartDate, "%Y-%m-%d") + datetime.timedelta(days=j)
            daytime = daytime.strftime("%Y-%m-%d %H:%M:%S").replace("-", "")[0:8];
            chinedaytime = str(int(daytime[0:4])-1911) + "/" + daytime[4:6] + "/" + daytime[6:8]
        print("chinedaytime=" , chinedaytime)
        r = requests.get("http://www.tpex.org.tw/web/stock/3insti/daily_trade/3itrade_hedge_result.php?l=zh-tw&se=EW&t=D&d=" + chinedaytime + "&_=1551422327244")
        d = json.loads(r.text)
        global k
        k = 5  # K來設定20171215前後資料格式不同
        z = 9
        # print(json.dumps(d["reportTitle"]))
        if json.dumps(d["reportTitle"]) != '""':
            item_dict = json.loads((json.dumps(d["aaData"][0], ensure_ascii=False)))
            if len(item_dict) == 25:
                k = 11
                z = 14
            item_dict2 = json.loads((json.dumps(d["aaData"], ensure_ascii=False)))
            for i in range(0, len(item_dict2)):
                stock_id = (json.dumps(d["aaData"][i][0], ensure_ascii=False))
                name = (json.dumps(d["aaData"][i][1], ensure_ascii=False))
                trade_date = daytime
                funds_buy = (json.dumps(d["aaData"][i][int(k)], ensure_ascii=False)).replace(",", "")
                funds_sell = (json.dumps(d["aaData"][i][int(k)+1], ensure_ascii=False)).replace(",", "")
                funds_sum = (json.dumps(d["aaData"][i][int(k)+2], ensure_ascii=False)).replace(",", "")
                selfEmployed_buy = (json.dumps(d["aaData"][i][int(z)], ensure_ascii=False)).replace(",", "")
                selfEmployed_sell = (json.dumps(d["aaData"][i][int(z)+1], ensure_ascii=False)).replace(",", "")
                selfEmployed_sum = (json.dumps(d["aaData"][i][int(z)+2], ensure_ascii=False)).replace(",", "")
                # print("(stock_id,name,trade_date,funds_buy,funds_sell,funds_sum)" , stock_id,name,trade_date,funds_buy,funds_sell,funds_sum)
                c1.execute( "INSERT INTO ThreeBigOtc (stock_id,name,trade_date,funds_buy,funds_sell,funds_sum,selfEmployed_buy,selfEmployed_sell,selfEmployed_sum) VALUES (" + stock_id + "," + name + "," + trade_date + "," + funds_buy + "," + funds_sell + "," + funds_sum + "," + selfEmployed_buy + "," + selfEmployed_sell + "," +selfEmployed_sum + ")")
                conn1.commit()
            print(daytime + "成功下載");
        else:
            print(daytime + "沒有下載到");
        conn1.close()
    print("櫃買爬完三大Operation done successfully");


# do_big_twse_three_big_OTC("2020-04-28", 1)
