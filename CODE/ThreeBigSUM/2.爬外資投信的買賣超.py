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
    r = requests.get( "https://www.twse.com.tw/fund/BFI82U?response=json&dayDate=" + daytime + "&type=day&_=1574870169125", headers=twse_html_headers)
    d = json.loads(r.text)
    if json.dumps(d["stat"], ensure_ascii=False) == '"OK"':
        trade_date = (json.dumps(d["date"], ensure_ascii=False)).replace("'", "").replace('"', '')
        funds_sum = (json.dumps(d["data"][2][3], ensure_ascii=False)).replace("'", "").replace('"', '').replace(",", "")
        foreign_sum = (json.dumps(d["data"][3][3], ensure_ascii=False)).replace("'", "").replace('"', '').replace(",","")
        if (int(trade_date) > 20171216):
            foreign_sum2 = (json.dumps(d["data"][4][3], ensure_ascii=False)).replace("'", "").replace('"', '').replace(",", "")
            foreign_sum = str(int(foreign_sum) + int(foreign_sum2))
        c.execute('UPDATE ThreeBigSum SET funds_sum =' + funds_sum + ',foreign_sum= ' + foreign_sum  +'  WHERE trade_date = ' + trade_date + '')
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