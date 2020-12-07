# encoding=UTF-8
import datetime
import sqlite3
import requests
import json
import time
import CODE.config


startDate = CODE.config.startDate
twse_html_headers = CODE.config.twse_html_headers


def DownloadOption_Put_process(daytime):
    time.sleep(5)
    conn1 = sqlite3.connect('C:/Users/user/Desktop/十大交易人/小胖下載加權指數報酬率Crawler/db/crawler.db')
    c1 = conn1.cursor()
    r = requests.get("https://datawinner.sysnet.net.tw/data/?s=TXO&f=conLongVol3p,conShortVol3p,conNetVol3p,top5BuyP,top5SellP,top10BuyP,top10SellP&d=" + daytime + "&o=0&t=0&alt=1&area=0A&token=u40wn2rubilwebfw10jddhlp")
    d = r.json()['d1']
    for x in d:
        if x["多方未平倉口數"] != None:
            trade_date = str(x["日期"])
            put_foreign_long = str(x["多方未平倉口數"])
            put_foreign_short = str(x["空方未平倉口數"])
            put_foreign_sum = str(x["多空未平倉口數"])
            put_long_top5 = str(x["前五大交易人買方部位"])
            put_short_top5 = str(x["前五大交易人賣方部位"])
            put_long_top10 = str(x["前十大交易人買方部位"])
            put_short_top10 = str(x["前十大交易人賣方部位"])
            c1.execute('UPDATE AllFutures SET put_foreign_long =' + put_foreign_long + '  , put_foreign_short=' + put_foreign_short + ' , put_foreign_sum=' + put_foreign_sum + ' , put_long_top5=' + put_long_top5 + ' , put_short_top5=' + put_short_top5 + ' , put_long_top10=' + put_long_top10 + ' , put_short_top10=' + put_short_top10 + ' WHERE trade_date =' + trade_date )
            conn1.commit()
            print(daytime + "選擇權賣權十大外資成功下載");
        # elif json.dumps(d["stat"], ensure_ascii=False) == '"查詢日期大於可查詢最大日期，請重新查詢!"':
        #     print(startDate + "請重新查詢");
        # elif json.dumps(d["stat"], ensure_ascii=False) == '"很抱歉，目前線上人數過多，請您稍候再試"':
        #     print(startDate + "執行重跑");
        #     do_big_twse_three_big(daytime)
        else:
            print(daytime + "選擇權賣權十大外資沒有下載到");
        conn1.close()


def DownloadOption_Put(tempstartDate, index):
    for j in range(0,index):
        daytimeTwo = "";
        if tempstartDate == 0:
            daytimeOne = time.strftime("%Y-%m-%d", time.localtime())
            daytimeTwo = daytimeOne.replace("-", "")[0:8];
        else:
            daytimeOne = datetime.datetime.strptime(tempstartDate, "%Y-%m-%d") + datetime.timedelta(days=j)
            daytimeTwo = daytimeOne.strftime("%Y-%m-%d %H:%M:%S").replace("-", "")[0:8];
        try:
            DownloadOption_Put_process(daytimeTwo)
        except requests.ConnectionError as e:
            print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
            print(str(e))
            DownloadOption_Put(str(daytimeOne)[0:10], index)
            continue
        except requests.RequestException as e:
            print("OOPS!! General Error")
            print(str(e))
            DownloadOption_Put(str(daytimeOne)[0:10], index)
            continue


# DownloadOption_Put("2020-09-29",1)