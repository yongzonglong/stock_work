# encoding=UTF-8
import datetime
import requests
import json
import time
import sqlite3
import CODE.config
startDate = CODE.config.startDate
twse_html_headers = CODE.config.twse_html_headers

def do_twse_three_big_price(daytime):
    conn = sqlite3.connect('C:/Users/user/Desktop/十大交易人/小胖下載加權指數報酬率Crawler/db/crawler.db')
    c = conn.cursor()
    time.sleep(5)
    r = requests.get( "http://www.twse.com.tw/exchangeReport/MI_INDEX?response=json&date=" + daytime + "&type=ALLBUT0999&_=1551356508238", headers=twse_html_headers)
    d = json.loads(r.text)
    if json.dumps(d["stat"], ensure_ascii=False) == '"OK"':
        trade_date = (json.dumps(d["date"], ensure_ascii=False))
        close = (json.dumps(d["data4"][1][1], ensure_ascii=False))
        c.execute('INSERT INTO ThreeBigSum (close,trade_date) VALUES (' + close + "," + trade_date + ")")
        conn.commit()
    conn.close()


def do_big_twse_three_big_price(tempstartDate):
    for j in range(0,2000):
        # print "j=",j
        print("tempstartDate=",tempstartDate)
        daytimeOne = datetime.datetime.strptime(tempstartDate, "%Y-%m-%d") + datetime.timedelta(days=j)
        daytimeTwo = daytimeOne.strftime("%Y-%m-%d %H:%M:%S").replace("-", "")[0:8];
        print("daytimeTwo=", daytimeTwo)
        try:
            do_twse_three_big_price(daytimeTwo)
        except requests.ConnectionError as e:
            print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
            print(str(e))
            time.sleep(30)
            do_big_twse_three_big_price(str(daytimeOne)[0:10])
        except requests.RequestException as e:
            print("OOPS!! General Error")
            print(str(e))
            time.sleep(30)
            do_big_twse_three_big_price(str(daytimeOne)[0:10])

do_big_twse_three_big_price(startDate)