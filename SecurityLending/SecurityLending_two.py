# encoding=UTF-8
import datetime
import requests
import json
import time
import sqlite3
import SecurityLending.config
from CODE.common_fumction.commom_proxy_ip import get_chrome_proxy

startDate = SecurityLending.config.startDate

# 去證交所爬借券賣出的股價

def do_twse_securitylending_price(daytime, index):
    conn = sqlite3.connect('C:/Users/user/Desktop/十大交易人/小胖下載加權指數報酬率Crawler/db/crawler.db')
    c = conn.cursor()
    if index != 0:
        time.sleep(5)
    url = "http://www.twse.com.tw/exchangeReport/MI_INDEX?response=json&date=" + daytime + "&type=ALLBUT0999& _=1551356508238"

    # r = requests.get( "http://www.twse.com.tw/exchangeReport/MI_INDEX?response=json&date=" + daytime + "&type=ALLBUT0999& _=1551356508238")
    # d = json.loads(r.text)

    d = json.loads(get_chrome_proxy(url))
    if json.dumps(d["stat"], ensure_ascii=False) == '"OK"':
        item_dict = json.loads(json.dumps(d["data9"]))
        #print "value=" , len(item_dict)
        for i in range(0, len(item_dict)):
           #print "i=" , i
           #print "leeeee=" , (json.dumps(d["data"][i][0], ensure_ascii=False)).replace("/", "")[4:8]
           close = (json.dumps(d["data9"][i][8], ensure_ascii=False))
           stock_id = (json.dumps(d["data9"][i][0], ensure_ascii=False))
           # print ("stock_id,daytime,close=",stock_id,daytime,close)
           c.execute('UPDATE SecurityLendingSell SET close_price =' + close + ' WHERE stock_id =' + stock_id + ' and trade_date = ' + daytime + '')
           conn.commit()
        print(daytime + "成功下載");
        conn.close()
    else:
        print(daytime + "沒有下載到外資借券的收盤價")


def do_twse_securitylending_num_price(tempstartDate,index):
    for j in range(0,index):
        daytimeTwo = "";
        if tempstartDate == 0:
            daytimeOne = time.strftime("%Y-%m-%d", time.localtime())
            daytimeTwo = daytimeOne.replace("-", "")[0:8];
        else:
            daytimeOne = datetime.datetime.strptime(tempstartDate, "%Y-%m-%d") + datetime.timedelta(days=j)
            daytimeTwo = daytimeOne.strftime("%Y-%m-%d %H:%M:%S").replace("-", "")[0:8];
        try:
            # print(daytimeTwo);
            do_twse_securitylending_price(daytimeTwo, index)
        except requests.ConnectionError as e:
            print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
            print(str(e))
            time.sleep(30)
            do_twse_securitylending_num_price(str(daytimeOne)[0:10], index)
            continue
        except requests.RequestException as e:
            print("OOPS!! General Error")
            print(str(e))
            time.sleep(30)
            do_twse_securitylending_num_price(str(daytimeOne)[0:10], index)
            continue


# do_twse_securitylending_num_price("2020-02-20",1)

# do_twse_securitylending_price("20201009",0)