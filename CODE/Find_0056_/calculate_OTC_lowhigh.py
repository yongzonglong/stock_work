import requests
import json
from datetime import date
import datetime
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
from CODE.LineNotify import lineNotifyMessage

# 判斷勝率
def _determine_ratio(sum_list):
    ratio = 0
    for i in range(len(sum_list)):
        if sum_list[i] >=0:
            ratio = ratio + 1
    return round(ratio/len(sum_list),3)


#取得櫃買指數
def _get_OTC( start_date, end_date):
    url = "https://datawinner.sysnet.net.tw/data/?s=TWNO0000&f=C&d=" + start_date + "," + end_date + "&o=0&t=0&alt=1&area=0A&token=byfrclqxxi4mmvqxb2nfstsc"
    r = requests.get(url)
    d = json.loads(r.text)
    close_list = []
    date_list = []
    data_return = pd.DataFrame(columns=['close', 'date'])
    if json.dumps(d["d1"], ensure_ascii=False) != '':
        item_dict = json.loads((json.dumps(d["d1"], ensure_ascii=False)))
        for i in range(0, len(item_dict)):
            close = (json.dumps(item_dict[i]["收盤"], ensure_ascii=False))
            date = (json.dumps(item_dict[i]["日期"], ensure_ascii=False)).replace('"', '')
            if close != 'null':
                close_list.append( round(  float (close) ,2))
                date_list.append(date)
    data_return['close'] = pd.Series(close_list)
    data_return['date'] = pd.Series(date_list)
    return data_return[::-1].reset_index()


# 取得櫃買指數
def _get_OTC_Exdividend( start_date, end_date):
    url = "https://datawinner.sysnet.net.tw/data/?s=TWNO0000&f=C&d=" + start_date + "," + end_date + "&o=0&t=0&alt=1&area=0A&token=byfrclqxxi4mmvqxb2nfstsc"
    r = requests.get(url)
    d = json.loads(r.text)
    close_list = []
    date_list = []
    data_return = pd.DataFrame(columns=['highStockclose', 'date'])
    if json.dumps(d["d1"], ensure_ascii=False) != '':
        item_dict = json.loads((json.dumps(d["d1"], ensure_ascii=False)))
        for i in range(0, len(item_dict)):
            close = (json.dumps(item_dict[i]["收盤"], ensure_ascii=False))
            date = (json.dumps(item_dict[i]["日期"], ensure_ascii=False)).replace('"', '')
            if close != 'null':
                close_list.append(round(float(close), 2))
                date_list.append(date)
    data_return['highStockclose'] = pd.Series(close_list)
    data_return['date'] = pd.Series(date_list)
    return data_return[::-1].reset_index(drop=True)

def _get_0056_diff(data_return,data_0056_return):

    data_return = data_return.merge(data_0056_return, left_on='date', right_on='date')
    # print(data_return.to_string() )
    delay_day = 175
    sum_list=[]

    for i in range(len(data_return)):
        if i + delay_day == len(data_return)-1:
            # print( str(i) )
            # print(data_return.iloc[i:i + delay_day].close)
            # print(data_return.iloc[i + delay_day].close)
            if (data_return.iloc[i + delay_day].close > np.percentile(data_return.iloc[i:i + delay_day].close,(100), interpolation='midpoint')):
                print("今日櫃買指數分位數為創175日內新高>100;今日為=" + str(data_return.iloc[i + delay_day].date) + ";櫃買指數為=" + str(data_return.iloc[i + delay_day].close) + ";最佳櫃買指數買進分位數為低於50賣出的分位數為95，所以請賣出")
                lineNotifyMessage("今日櫃買指數分位數為創175日內新高>100;今日為=" + str(data_return.iloc[i + delay_day].date) + ";櫃買指數為=" + str(data_return.iloc[i + delay_day].close) + ";最佳櫃買指數買進分位數為低於50賣出的分位數為95，所以請賣出", 1)
                lineNotifyMessage("今日櫃買指數分位數為創175日內新高>100;今日為=" + str(data_return.iloc[i + delay_day].date) + ";櫃買指數為=" + str(data_return.iloc[i + delay_day].close) + ";最佳櫃買指數買進分位數為低於50賣出的分位數為95，所以請賣出", 2)
                lineNotifyMessage("今日櫃買指數分位數為創175日內新高>100;今日為=" + str(data_return.iloc[i + delay_day].date) + ";櫃買指數為=" + str(data_return.iloc[i + delay_day].close) + ";最佳櫃買指數買進分位數為低於50賣出的分位數為95，所以請賣出", 3)
            if (data_return.iloc[i + delay_day].close < np.percentile(data_return.iloc[i:i + delay_day ].close, (0),interpolation='midpoint')):
                lineNotifyMessage("今日櫃買指數分位數為創175日內新低<0;今日為=" + str(data_return.iloc[i + delay_day].date) + ";櫃買指數為=" + str(data_return.iloc[i + delay_day].close) + ";最佳櫃買指數買進分位數為低於50賣出的分位數為95，所以請買入", 1)
                lineNotifyMessage("今日櫃買指數分位數為創175日內新低<0;今日為=" + str(data_return.iloc[i + delay_day].date) + ";櫃買指數為=" + str(data_return.iloc[i + delay_day].close) + ";最佳櫃買指數買進分位數為低於50賣出的分位數為95，所以請買入", 2)
                lineNotifyMessage("今日櫃買指數分位數為創175日內新低<0;今日為=" + str(data_return.iloc[i + delay_day].date) + ";櫃買指數為=" + str(data_return.iloc[i + delay_day].close) + ";最佳櫃買指數買進分位數為低於50賣出的分位數為95，所以請買入", 3)
                print("今日櫃買指數分位數為創175日內新低<0;今日為=" + str(data_return.iloc[i + delay_day].date) + ";櫃買指數為=" + str(data_return.iloc[i + delay_day].close) + ";最佳櫃買指數買進分位數為低於50賣出的分位數為95，所以請買入")
            for j in range(0,100,1):
                if ( data_return.iloc[i+delay_day].close <= np.percentile(data_return.iloc[i:i + delay_day].close, (j+1), interpolation='midpoint') ):
                    if (data_return.iloc[i + delay_day].close >= np.percentile(data_return.iloc[i:i + delay_day ].close, (j), interpolation='midpoint')):
                        # print(str(data_return.iloc[i + delay_day].close))
                        # print(str(data_return.iloc[i]))
                        # print(str(data_return.iloc[i:i + 2]))
                        # print(str(np.percentile(data_return.iloc[i:i + delay_day-1].close, (100), interpolation='midpoint') ))
                        lineNotifyMessage("今日櫃買指數分位數為=" + str(j) + ";今日為=" + str(data_return.iloc[i + delay_day].date) + ";櫃買指數為=" + str(data_return.iloc[i + delay_day].close) + ";最佳買進分位數為低於50賣出的分位數為95", 1)
                        lineNotifyMessage("今日櫃買指數分位數為=" + str(j) + ";今日為=" + str(data_return.iloc[i + delay_day].date) + ";櫃買指數為=" + str(data_return.iloc[i + delay_day].close) + ";最佳買進分位數為低於50賣出的分位數為95", 2)
                        lineNotifyMessage("今日櫃買指數分位數為=" + str(j) + ";今日為=" + str(data_return.iloc[i + delay_day].date) + ";櫃買指數為=" + str(data_return.iloc[i + delay_day].close) + ";最佳買進分位數為低於50賣出的分位數為95", 3)
                        print("今日櫃買指數分位數為=" + str(j) + ";今日為=" + str(data_return.iloc[i+delay_day].date) + ";櫃買指數為=" + str(data_return.iloc[i+delay_day].close) + ";最佳買進分位數為低於50賣出的分位數為95")
    # return sum_list

def calculact_OTC_lowhigh_run(index):
    start_date = '20190101'
    # end_date = '20200603'
    daytimeOne = time.strftime("%Y-%m-%d", time.localtime())
    end_date = daytimeOne.replace("-", "")[0:8];
    data_return = _get_OTC(start_date, end_date)
    # data_return = _get_TWSE(start_date, end_date)
    # data_return = _get_high(start_date, end_date)
    # data_return = _get_high_Exdividend(start_date, end_date)
    # data_0056_return = _get_high0056(start_date, end_date)
    # 還原0056的除息
    data_0056_return = _get_OTC_Exdividend(start_date, end_date)
    _get_0056_diff(data_return, data_0056_return)

# calculact_OTC_lowhigh_run(0)
