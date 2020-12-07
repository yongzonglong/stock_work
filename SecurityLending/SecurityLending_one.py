# encoding=UTF-8
import datetime
import sqlite3
import requests
import json
import time
import SecurityLending.config
from CODE.common_fumction.commom_proxy_ip import get_chrome_proxy
startDate = SecurityLending.config.startDate

# 去證交所爬借券賣出

def do_twse_securitylending(daytime, index):
    if index != 0:
        time.sleep(5)
    conn1 = sqlite3.connect('C:/Users/user/Desktop/十大交易人/小胖下載加權指數報酬率Crawler/db/crawler.db')
    c1 = conn1.cursor()
    url = "http://www.twse.com.tw/exchangeReport/TWT93U?response=json&date=" + daytime + "&_=1551965717789"
    # r = requests.get("http://www.twse.com.tw/exchangeReport/TWT93U?response=json&date=" + daytime + "&_=1551965717789")
    # d = json.loads(r.text)

    d = json.loads(get_chrome_proxy(url))
    # global k
    # k = 5  # K來設定20171215前後資料格式不同
    # if  json.dumps(d["stat"], ensure_ascii=False) == '"OK"':
    #     if len(json.dumps(d["fields"])) == 1156:
    #         k = 8
    # print(json.dumps(d["date"], ensure_ascii=False))
    if json.dumps(d["stat"], ensure_ascii=False) == '"OK"':
        item_dict = json.loads((json.dumps(d["data"], ensure_ascii=False)))
        if len(item_dict) >10:
            for i in range(0, len(item_dict)):
                stock_id = (json.dumps(d["data"][i][0], ensure_ascii=False))
                name = (json.dumps(d["data"][i][1], ensure_ascii=False))
                trade_date = (json.dumps(d["date"], ensure_ascii=False))
                security_lending_sell = (json.dumps(d["data"][i][9], ensure_ascii=False)).replace(",", "")
                security_lending_back = (json.dumps(d["data"][i][10], ensure_ascii=False)).replace(",", "")
                c1.execute( "INSERT INTO SecurityLendingSell (stock_id,name,trade_date,security_lending_sell,security_lending_back) VALUES (" + stock_id + "," + name + "," + trade_date + "," + security_lending_sell + "," + security_lending_back + ")")
                conn1.commit()
            print(daytime + "成功下載");
    elif json.dumps(d["stat"], ensure_ascii=False) == '"查詢日期大於可查詢最大日期，請重新查詢!"':
        print(startDate + "請重新查詢");
    else:
        print(daytime + "沒有下載到外資借券")
    conn1.close()


def do_twse_securitylending_num(tempstartDate,index):
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
            do_twse_securitylending(daytimeTwo, index)
        except requests.ConnectionError as e:
            print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
            print(str(e))
            time.sleep(30)
            do_twse_securitylending_num(str(daytimeOne)[0:10], index)
            continue
        except requests.RequestException as e:
            print("OOPS!! General Error")
            print(str(e))
            time.sleep(30)
            do_twse_securitylending_num(str(daytimeOne)[0:10], index)
            continue



# do_twse_securitylending_num("2020-02-20",1)

# do_twse_securitylending("20201009",0)