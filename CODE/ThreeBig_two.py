# encoding=UTF-8
import datetime
import requests
import json
import time
import sqlite3
import CODE.config
from CODE.common_fumction.commom_proxy_ip import get_chrome_proxy


startDate = CODE.config.startDate
twse_html_headers = CODE.config.twse_html_headers
from CODE.LineNotify import lineNotifyMessage
new_twse_html_headers = CODE.config.new_twse_html_headers

# 爬證交所的股價


def do_twse_three_big_price(daytime, index):
    conn = sqlite3.connect('C:/Users/user/Desktop/十大交易人/小胖下載加權指數報酬率Crawler/db/crawler.db')
    c = conn.cursor()
    url = "http://www.twse.com.tw/exchangeReport/MI_INDEX?response=json&date=" + daytime + "&type=ALLBUT0999"
    # r = requests.get( "http://www.twse.com.tw/exchangeReport/MI_INDEX?response=json&date=" + daytime + "&type=ALLBUT0999", headers=new_twse_html_headers)
    # d = json.loads(r.text)
    # time.sleep(10)

    value = get_chrome_proxy(url)
    # print(value)
    d = json.loads(value)

    if json.dumps(d["stat"], ensure_ascii=False) == '"OK"':
        item_dict = json.loads(json.dumps(d["data9"]))
        #print "value=" , len(item_dict)
        for i in range(0, len(item_dict)):
           close = (json.dumps(d["data9"][i][8], ensure_ascii=False))
           stock_id = (json.dumps(d["data9"][i][0], ensure_ascii=False))
           volume = (json.dumps(d["data9"][i][2], ensure_ascii=False)).replace(",", "")
           # print ("volume=",volume[0:len(volume)-3])
           c.execute('UPDATE ThreeBig SET close_price =' + close + '  , volume = ' + volume + '  WHERE stock_id =' + stock_id + ' and trade_date = ' + daytime + '')
           conn.commit()
    conn.close()
    print("日期=", daytime, "成功下載。證交爬完股價")

def do_big_twse_three_big_price(tempstartDate, index):
    for j in range(0,index):
        daytimeTwo = 0;
        if tempstartDate == 00:
            daytimeOne = time.strftime("%Y-%m-%d", time.localtime())
            daytimeTwo = daytimeOne.replace("-", "")[0:8];
            # lineNotifyMessage("爬完證交所",1)
        else:
            daytimeOne = datetime.datetime.strptime(tempstartDate, "%Y-%m-%d") + datetime.timedelta(days=j)
            daytimeTwo = daytimeOne.strftime("%Y-%m-%d %H:%M:%S").replace("-", "")[0:8];
        try:
            do_twse_three_big_price(daytimeTwo, index)
        except requests.ConnectionError as e:
            print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
            print(str(e))
            time.sleep(30)
            do_big_twse_three_big_price(str(daytimeOne)[0:10], index)
        except requests.RequestException as e:
            print("OOPS!! General Error")
            print(str(e))
            time.sleep(30)
            do_big_twse_three_big_price(str(daytimeOne)[0:10], index)

# do_big_twse_three_big_price("2020-09-04", 1)

# do_twse_three_big_price("20201123", 1)