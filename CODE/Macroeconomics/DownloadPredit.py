# encoding=UTF-8
import datetime
import sqlite3
import requests
import json
import time
import CODE.config
import calendar


startDate = CODE.config.startDate
twse_html_headers = CODE.config.twse_html_headers

def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year,month)[1])
    return datetime.date(year, month, day)


def Download_Predict_process(daytime):
    conn1 = sqlite3.connect('C:/Users/user/Desktop/十大交易人/小胖下載加權指數報酬率Crawler/db/crawler.db')
    conn2 = sqlite3.connect('C:/Users/user/Desktop/十大交易人/小胖下載加權指數報酬率Crawler/db/crawler.db')
    c1 = conn1.cursor()
    c2 = conn2.cursor()
    print(daytime);
    r = requests.get("https://datawinner.sysnet.net.tw/data/?s=TWN.CY&f=ECLIGHT,LEADINGIDX,CONIDX,PMI&d=" + daytime + "&o=0&t=0&alt=1&area=0A&token=u40wn2rubilwebfw10jddhlp")
    d = r.json()['d1']
    for x in d:
        if x["日期"] != None and x["景氣對策綜合判斷分數"] != None and  x["領先指標"] != None and  x["同時指標"] != None and x["製造業採購經理人指數"] != None:
            trade_date = str(x["日期"])
            monitoring_indicator = str(x["景氣對策綜合判斷分數"])
            monitoring_leading_indicator = str(x["領先指標"])
            monitoring_simultaneous_indicator = str(x["同時指標"])
            purchasing_managers_Index = str(x["製造業採購經理人指數"])
            c1.execute( "INSERT INTO Macroeconomics2 (trade_date,monitoring_indicator,monitoring_leading_indicator,monitoring_simultaneous_indicator,purchasing_managers_Index) VALUES (" + trade_date + "," + monitoring_indicator+ "," + monitoring_leading_indicator + "," + monitoring_simultaneous_indicator + "," + purchasing_managers_Index +  ")")
            conn1.commit()
            print(daytime + "台幣景氣指標成功下載");
        else:
            print(daytime + "台幣景氣指標沒有下載到");
    time.sleep(5)
    conn1.close()


def Download_Predict(index):
    for j in range(0,index):
        conn2 = sqlite3.connect('C:/Users/user/Desktop/十大交易人/小胖下載加權指數報酬率Crawler/db/crawler.db')
        c2 = conn2.cursor()
        cursor2 = c2.execute(' select * from Macroeconomics2')
        lasttime = ""
        for row2 in cursor2:
            # print(row2[0])
            lasttime = str(row2[0])
        # print("lasttime=" + lasttime )
        if lasttime == "":
            lasttime = "2018-01-01"
        else:
            lasttime = lasttime[0:4] + "-" + lasttime[4:6] + "-01"
            lasttime = datetime.datetime.strptime(lasttime, "%Y-%m-%d")
            lasttime = str(add_months(lasttime, 1))
        lasttime = lasttime.replace("-", "")[0:8];
        try:
            conn2.close()
            Download_Predict_process(lasttime)
        except requests.ConnectionError as e:
            print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
            print(str(e))
            Download_Predict(index)
            continue
        except requests.RequestException as e:
            print("OOPS!! General Error")
            print(str(e))
            Download_Predict(index)
            continue


# Download_Predict(30)