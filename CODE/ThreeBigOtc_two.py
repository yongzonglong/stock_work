# encoding=UTF-8
import datetime
import requests
import json
import time
import sqlite3
import CODE.config
from CODE.LineNotify import lineNotifyMessage


# 爬櫃買中心的股價


startDate = CODE.config.startDate
def do_big_twse_three_big_price_OTC(tempstartDate, index):
    conn = sqlite3.connect('C:/Users/user/Desktop/十大交易人/小胖下載加權指數報酬率Crawler/db/crawler.db')
    c = conn.cursor()
    for j in range(0,index):
        time.sleep(2)
        if tempstartDate == 0:
            daytimeOne = time.strftime("%Y-%m-%d", time.localtime())
            daytimeTwo = daytimeOne.replace("-", "")[0:8];
            daytime = daytimeTwo
            chinedaytime = str(int(daytimeTwo[0:4]) - 1911) + "/" + daytimeTwo[4:6] + "/" + daytimeTwo[6:8]
        else:
            daytime = datetime.datetime.strptime(tempstartDate, "%Y-%m-%d") + datetime.timedelta(days=j)
            daytime = daytime.strftime("%Y-%m-%d %H:%M:%S").replace("-", "")[0:8];
            chinedaytime = str(int(daytime[0:4]) - 1911) + "/" + daytime[4:6] + "/" + daytime[6:8]
        r = requests.get("http://www.tpex.org.tw/web/stock/aftertrading/otc_quotes_no1430/stk_wn1430_result.php?l=zh-tw&d=" + chinedaytime + "&se=EW&_=1551457899559")
        d = json.loads(r.text)
        if json.dumps(d["aaData"]) != []:
            print("櫃買爬完股價成交量。日期=",daytime)
            item_dict = json.loads(json.dumps(d["aaData"]))
            #print "value=" , len(item_dict)
            for i in range(0, len(item_dict)):
               #print "i=" , i
               #print "leeeee=" , (json.dumps(d["data"][i][0], ensure_ascii=False)).replace("/", "")[4:8]
               close = (json.dumps(d["aaData"][i][2], ensure_ascii=False))
               stock_id = (json.dumps(d["aaData"][i][0], ensure_ascii=False))
               volume = (json.dumps(d["aaData"][i][7], ensure_ascii=False)).replace(",", "")
               # print ("stock_id,daytime,close=",stock_id,daytime,close)
               c.execute('UPDATE ThreeBigOtc SET close_price =' + close + '  , volume = ' + volume + '  WHERE stock_id =' + stock_id + ' and trade_date = ' + daytime + '')
               conn.commit()
    print("櫃買爬完股價Operation done successfully");
    # lineNotifyMessage("爬完櫃買中心", 1)
    conn.close()

# do_big_twse_three_big_price_OTC("2020-04-28",1)