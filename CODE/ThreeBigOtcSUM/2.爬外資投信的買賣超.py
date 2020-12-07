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
    chinedaytime = str(int(daytime[0:4])-1911) + "/" + daytime[4:6] + "/" + daytime[6:8]
    c = conn.cursor()
    time.sleep(5)
    r = requests.get("https://www.tpex.org.tw/web/stock/3insti/3insti_summary/3itrdsum_result.php?l=zh-tw&t=D&p=1&d=" + chinedaytime + "&_=1575305535578", headers=twse_html_headers)
    d = json.loads(r.text)
    if json.dumps(d["iTotalRecords"], ensure_ascii=False) != '0':
        trade_date = daytime
        funds_sum = (json.dumps(d["aaData"][2][3], ensure_ascii=False)).replace("'", "").replace('"', '').replace(",", "")
        foreign_sum = (json.dumps(d["aaData"][1][3], ensure_ascii=False)).replace("'", "").replace('"', '').replace(",","")
        if (int(trade_date) > 20180113):
            funds_sum = (json.dumps(d["aaData"][6][3], ensure_ascii=False)).replace("'", "").replace('"', '').replace(",","")
            foreign_sum = (json.dumps(d["aaData"][5][3], ensure_ascii=False)).replace("'", "").replace('"', '').replace(",", "")
        c.execute('UPDATE ThreeBigOtcSum SET funds_sum =' + funds_sum + ',foreign_sum= ' + foreign_sum  +'  WHERE trade_date = ' + trade_date + '')
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