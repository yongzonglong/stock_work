# encoding=UTF-8
import datetime
import sqlite3
import requests
import json
import time
import CODE.config


startDate = CODE.config.startDate
twse_html_headers = CODE.config.twse_html_headers


def Download_USD_process(daytime):
    conn1 = sqlite3.connect('C:/Users/user/Desktop/十大交易人/小胖下載加權指數報酬率Crawler/db/crawler.db')
    c1 = conn1.cursor()
    r = requests.get("https://datawinner.sysnet.net.tw/data/?s=TWD.FX&f=USDCLOSE&d=" + daytime + "&o=2&t=0&alt=1&area=0A&token=u40wn2rubilwebfw10jddhlp")
    d = r.json()['d1']
    for x in d:
        if x[daytime] != None:
            trade_date = str(daytime)
            USD = str(x[daytime])
            c1.execute( "INSERT INTO Macroeconomics (trade_date,USD) VALUES (" + trade_date + "," + USD +  ")")
            conn1.commit()
            print(daytime + "台幣匯率成功下載");
        # elif json.dumps(d["stat"], ensure_ascii=False) == '"查詢日期大於可查詢最大日期，請重新查詢!"':
        #     print(startDate + "請重新查詢");
        # elif json.dumps(d["stat"], ensure_ascii=False) == '"很抱歉，目前線上人數過多，請您稍候再試"':
        #     print(startDate + "執行重跑");
        #     do_big_twse_three_big(daytime)
        else:
            print(daytime + "台幣匯率沒有下載到");
    time.sleep(5)
    conn1.close()


def Download_USD(tempstartDate, index):
    for j in range(0,index):
        daytimeTwo = "";
        if tempstartDate == 0:
            daytimeOne = time.strftime("%Y-%m-%d", time.localtime())
            daytimeTwo = daytimeOne[0:11]
            daytimeOne = datetime.datetime.strptime(daytimeTwo, "%Y-%m-%d") - datetime.timedelta(days=1)
            daytimeTwo = daytimeOne.strftime("%Y-%m-%d %H:%M:%S").replace("-", "")[0:8]
        else:
            daytimeOne = datetime.datetime.strptime(tempstartDate, "%Y-%m-%d") + datetime.timedelta(days=j)
            daytimeTwo = daytimeOne.strftime("%Y-%m-%d %H:%M:%S").replace("-", "")[0:8];
        try:
            Download_USD_process(daytimeTwo)
        except requests.ConnectionError as e:
            print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
            print(str(e))
            Download_USD(str(daytimeOne)[0:10], index)
            continue
        except requests.RequestException as e:
            print("OOPS!! General Error")
            print(str(e))
            Download_USD(str(daytimeOne)[0:10], index)
            continue


# Download_USD("2020-02-20",1)