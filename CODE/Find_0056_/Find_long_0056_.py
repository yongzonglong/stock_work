
import requests
import json
from datetime import date
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# 判斷勝率
def _determine_ratio(sum_list):
    ratio = 0
    for i in range(len(sum_list)):
        if sum_list[i] >=0:
            ratio = ratio + 1
    return round(ratio/len(sum_list),3)

# 取得有還原的0056
def _get_high_Exdividend(stock_id ,start_date, end_date):
    url = "https://datawinner.sysnet.net.tw/data/?s=" + stock_id + "&f=%E6%94%B6%E7%9B%A4(%E9%82%84%E5%8E%9F)%40C:ADJ()&d=" + start_date + "," + end_date + "&o=0&t=0&alt=1&area=0A&token=byfrclqxxi4mmvqxb2nfstsc"
    r = requests.get(url)
    d = json.loads(r.text)
    close_list = []
    date_list = []
    data_return = pd.DataFrame(columns=['close', 'date'])
    if json.dumps(d["d1"], ensure_ascii=False) != '':
        item_dict = json.loads((json.dumps(d["d1"], ensure_ascii=False)))
        for i in range(0, len(item_dict)):
            close = (json.dumps(item_dict[i]["收盤(還原)"], ensure_ascii=False))
            date = (json.dumps(item_dict[i]["日期"], ensure_ascii=False)).replace('"', '')
            if close != 'null':
                close_list.append(round(float(close), 2))
                date_list.append(date)
    data_return['close'] = pd.Series(close_list)
    data_return['date'] = pd.Series(date_list)
    return data_return[::-1].reset_index()

# 取得有還原的0056
def _get_high0056_Exdividend( start_date, end_date):
    url = "https://datawinner.sysnet.net.tw/data/?s=0056&f=%E6%94%B6%E7%9B%A4(%E9%82%84%E5%8E%9F)%40C:ADJ()&d=" + start_date + "," + end_date + "&o=0&t=0&alt=1&area=0A&token=byfrclqxxi4mmvqxb2nfstsc"
    r = requests.get(url)
    d = json.loads(r.text)
    close_list = []
    date_list = []
    data_return = pd.DataFrame(columns=['highStockclose', 'date'])
    if json.dumps(d["d1"], ensure_ascii=False) != '':
        item_dict = json.loads((json.dumps(d["d1"], ensure_ascii=False)))
        for i in range(0, len(item_dict)):
            close = (json.dumps(item_dict[i]["收盤(還原)"], ensure_ascii=False))
            date = (json.dumps(item_dict[i]["日期"], ensure_ascii=False)).replace('"', '')
            if close != 'null':
                close_list.append(round(float(close), 2))
                date_list.append(date)
    data_return['highStockclose'] = pd.Series(close_list)
    data_return['date'] = pd.Series(date_list)
    return data_return[::-1].reset_index()

def _get_0056_diff(lowTh, upTh, data_return, data_0056_return, delay_day, buy_start_date):
    data_return = data_return.merge(data_0056_return, how='left', left_on='date', right_on='date')
    highStcok = 0
    highStcokPrice = 0
    # delay_day = 50
    print(data_return.to_string())
    sum_list = []
    for i in range(len(data_return)):
        if i + delay_day < len(data_return):
            if data_return.iloc[i + delay_day].date >= buy_start_date:
                # print(data_return.iloc[i + delay_day].date)
                # print("分位數LOW=" +  str( np.percentile(data_return.iloc[i:i + delay_day - 1].close,
                #                                                           (lowTh), interpolation='midpoint')) )
                # print("分位數UP=" + str(np.percentile(data_return.iloc[i:i + delay_day - 1].close,
                #                                 (upTh), interpolation='midpoint')) )
                if (data_return.iloc[i + delay_day].close < np.percentile(data_return.iloc[i:i + delay_day].close,
                                                                          (lowTh), interpolation='midpoint')) & (
                        highStcok == 0):
                    highStcok = 1
                    highStcokPrice = data_return.iloc[i + delay_day].highStockclose
                    print("買進0056日=" + str(data_return.iloc[i + delay_day].date) + "股價=" + str(
                        data_return.iloc[i + delay_day].highStockclose))
                    # print(data_return.iloc[i:i + delay_day].close.to_string() )
                elif (data_return.iloc[i + delay_day].close > np.percentile(data_return.iloc[i:i + delay_day].close,
                                                                            (upTh), interpolation='midpoint')) & (
                        highStcok == 1):
                    highStcok = 0
                    print("賣進0056日=" + str(data_return.iloc[i + delay_day].date) + "股價=" + str(
                        data_return.iloc[i + delay_day].highStockclose))
                    print("損益=" + str(float(data_return.iloc[i + delay_day].highStockclose) - float(highStcokPrice)))
                    sum_list.append(float(data_return.iloc[i + delay_day].highStockclose) - float(highStcokPrice))
                elif (i + delay_day == len(data_return) - 1) & highStcok == 1:
                    print("最後一天，賣進0056日=" + str(data_return.iloc[i + delay_day].date) + "股價=" + str(
                        data_return.iloc[i + delay_day].highStockclose))
                    highStcok = 0
                    print("損益=" + str(float(data_return.iloc[i + delay_day].highStockclose) - float(highStcokPrice)))
                    sum_list.append(float(data_return.iloc[i + delay_day].highStockclose) - float(highStcokPrice))
    # print(sum_list)
    # print( sum(sum_list)  )
    print("總損益=" + str(sum(sum_list)) + ";勝率=" + str(_determine_ratio(sum_list)))
    # return sum(sum_list), _determine_ratio(sum_list) * 100
if __name__ == '__main__':
    data_start_date = '20170101'
    data_end_date = '20200703'
    buy_start_date = '20180101'
    delay_day = 190

    # data_return = _get_OTC(data_start_date, data_end_date)
    # data_return = _get_TWSE(data_start_date, data_end_date)
    data_return = _get_high_Exdividend("0056", data_start_date, data_end_date)


    # 還原0056的除息
    data_0056_return = _get_high0056_Exdividend(data_start_date, data_end_date)



    _get_0056_diff(50, 95, data_return, data_0056_return, delay_day, buy_start_date)


