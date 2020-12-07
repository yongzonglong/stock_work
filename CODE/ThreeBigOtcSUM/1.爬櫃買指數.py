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
    chinedaytime = str(int(daytime[0:4])-1911) + "/" + daytime[4:6] + "/" + daytime[6:8]
    conn = sqlite3.connect('C:/Users/user/Desktop/十大交易人/小胖下載加權指數報酬率Crawler/db/crawler.db')
    c = conn.cursor()
    time.sleep(5)
    r = requests.get( "https://www.tpex.org.tw/web/stock/aftertrading/index_summary/summary_result.php?l=zh-tw&d=" + chinedaytime + "&_=1575273615311", headers=twse_html_headers)
    d = json.loads(r.text)
    if json.dumps(d["iTotalRecords"], ensure_ascii=False) != '0':
        trade_date = daytime
        close = (json.dumps(d["aaData"][0][1], ensure_ascii=False))
        c.execute('INSERT INTO ThreeBigOtcSum (close,trade_date) VALUES (' + close + "," + trade_date + ")")
        conn.commit()
    conn.close()


def do_big_twse_three_big_price(tempstartDate):
    for j in range(0,2000):
        # print "j=",j
        print "tempstartDate=",tempstartDate
        daytimeOne = datetime.datetime.strptime(tempstartDate, "%Y-%m-%d") + datetime.timedelta(days=j)
        daytimeTwo = daytimeOne.strftime("%Y-%m-%d %H:%M:%S").replace("-", "")[0:8];
        print "daytimeTwo=", daytimeTwo
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