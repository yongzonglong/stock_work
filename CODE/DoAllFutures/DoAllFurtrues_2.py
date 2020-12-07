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
import random
new_twse_html_headers  = CODE.config.new_twse_html_headers
no_cookie_twse_html_headers = CODE.config.no_cookie_twse_html_headers

def do_AllFurtrues_process_price(daytime):
    conn = sqlite3.connect('C:/Users/user/Desktop/十大交易人/小胖下載加權指數報酬率Crawler/db/crawler.db')
    c = conn.cursor()
    # r = requests.get( "http://www.twse.com.tw/exchangeReport/MI_INDEX?response=json&date=" + daytime + "&type=ALLBUT0999&_=1601889071186" , headers=no_cookie_twse_html_headers)
    # d = json.loads(r.text)

    url = "http://www.twse.com.tw/exchangeReport/MI_INDEX?response=json&date=" + daytime + "&type=ALLBUT0999&_=1601889071186"
    value = get_chrome_proxy(url)
    print(value)
    d = json.loads(value)

    # time.sleep(10)
    if json.dumps(d["stat"], ensure_ascii=False) == '"OK"':
        trade_date = (json.dumps(d["date"], ensure_ascii=False))
        close = (json.dumps(d["data4"][1][1], ensure_ascii=False))
        c.execute('UPDATE AllFutures SET close =' + close + '  WHERE trade_date =' + trade_date )
        conn.commit()
        print(daytime + "成功下載");
    else:
        print(daytime + "外資十大交易人沒有下載到加權指數");
    conn.close()


def do_AllFurtrues_price(tempstartDate, index):
    for j in range(0,index):
        daytimeTwo = "";
        if tempstartDate == 0:
            daytimeOne = time.strftime("%Y-%m-%d", time.localtime())
            daytimeTwo = daytimeOne.replace("-", "")[0:8];
        else:
            daytimeOne = datetime.datetime.strptime(tempstartDate, "%Y-%m-%d") + datetime.timedelta(days=j)
            daytimeTwo = daytimeOne.strftime("%Y-%m-%d %H:%M:%S").replace("-", "")[0:8];
        try:
            do_AllFurtrues_process_price(daytimeTwo)
        except requests.ConnectionError as e:
            print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
            print(str(e))
            time.sleep(30)
            do_AllFurtrues_price(str(daytimeOne)[0:10], index)
        except requests.RequestException as e:
            print("OOPS!! General Error")
            print(str(e))
            time.sleep(30)
            do_AllFurtrues_price(str(daytimeOne)[0:10], index)

# do_AllFurtrues_price("2020-10-12", 1)

# do_AllFurtrues_process_price("20201013")