# encoding=UTF-8
import datetime
import sqlite3
import requests
import json
import time
import CODE.config
from CODE.common_fumction.commom_proxy_ip import get_chrome_proxy

startDate = CODE.config.startDate
twse_html_headers = CODE.config.twse_html_headers
new_twse_html_headers = CODE.config.new_twse_html_headers

# 爬證交所的三大法人

def do_twse_three_big(daytime, index):
    conn1 = sqlite3.connect('C:/Users/user/Desktop/十大交易人/小胖下載加權指數報酬率Crawler/db/crawler.db')
    c1 = conn1.cursor()
    url = "https://www.twse.com.tw/fund/T86?response=json&date=" + (daytime) + "&selectType=ALLBUT0999&_=1601372225479"
    # rs = requests.Session()
    # r = requests.get(url, headers=new_twse_html_headers)
    # d = json.loads(r.text)

    d =  json.loads(str(get_chrome_proxy(url)))
    # d =  get_chrome_proxy(url)
    # time.sleep(10)
    # print(d)
    global k
    k = 5  # K來設定20171215前後資料格式不同
    if  json.dumps(d["stat"], ensure_ascii=False) == '"OK"':
        if len(json.dumps(d["fields"])) == 1156:
            k = 8
    print( json.dumps(d["stat"], ensure_ascii=False))
    if json.dumps(d["stat"], ensure_ascii=False) == '"OK"':
        item_dict = json.loads((json.dumps(d["data"], ensure_ascii=False)))
        for i in range(0, len(item_dict)):
            stock_id = (json.dumps(d["data"][i][0], ensure_ascii=False))
            name = (json.dumps(d["data"][i][1], ensure_ascii=False))
            trade_date = (json.dumps(d["date"], ensure_ascii=False))
            funds_buy = (json.dumps(d["data"][i][int(k)], ensure_ascii=False)).replace(",", "")
            funds_sell = (json.dumps(d["data"][i][int(k)+1], ensure_ascii=False)).replace(",", "")
            funds_sum = (json.dumps(d["data"][i][int(k)+2], ensure_ascii=False)).replace(",", "")
            selfEmployed_buy = (json.dumps(d["data"][i][int(k+4)], ensure_ascii=False)).replace(",", "")
            selfEmployed_sell = (json.dumps(d["data"][i][int(k)+5], ensure_ascii=False)).replace(",", "")
            selfEmployed_sum = (json.dumps(d["data"][i][int(k)+6], ensure_ascii=False)).replace(",", "")
            c1.execute( "INSERT INTO ThreeBig (stock_id,name,trade_date,funds_buy,funds_sell,funds_sum,selfEmployed_buy,selfEmployed_sell,selfEmployed_sum) VALUES (" + stock_id + "," + name + "," + trade_date + "," + funds_buy + "," + funds_sell + "," + funds_sum + "," + selfEmployed_buy + "," + selfEmployed_sell + "," +selfEmployed_sum + ")")
            conn1.commit()
    elif json.dumps(d["stat"], ensure_ascii=False) == '"查詢日期大於可查詢最大日期，請重新查詢!"':
        print(startDate + "請重新查詢");
    elif json.dumps(d["stat"], ensure_ascii=False) == '"很抱歉，目前線上人數過多，請您稍候再試"':
        print(startDate + "執行重跑");
        do_big_twse_three_big(daytime, index)
    else:
        print(daytime + "沒有下載到");
    print(daytime + "成功下載。證交爬完三大");
    conn1.close()


def do_big_twse_three_big(tempstartDate,index):
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
            do_twse_three_big(daytimeTwo,index)
        except requests.ConnectionError as e:
            print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
            print(str(e))
            time.sleep(30)
            do_big_twse_three_big(str(daytimeOne)[0:10], index)
            continue
        except requests.RequestException as e:
            print("OOPS!! General Error")
            print(str(e))
            time.sleep(30)
            do_big_twse_three_big(str(daytimeOne)[0:10], index)
            continue

# do_big_twse_three_big("2020-09-28",1)

# do_twse_three_big("20201123", 1)