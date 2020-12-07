import requests
import json
from datetime import date
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import product
from concurrent import futures
import os
from tqdm import tqdm


# 判斷勝率
def _determine_ratio(sum_list):
    ratio = 0
    for i in range(len(sum_list)):
        if sum_list[i] > 0:
            ratio = ratio + 1
    return round(ratio / len(sum_list), 3)

# 取得有還原的0050
def _get_high_Exdividend(stock_id, start_date, end_date):
    url = "https://datawinner.sysnet.net.tw/data/?s=" + stock_id + "&f=%E6%94%B6%E7%9B%A4(%E9%82%84%E5%8E%9F)%40C:ADJ(),%E9%96%8B%E7%9B%A4(%E9%82%84%E5%8E%9F)%40O:ADJ(),%E6%9C%80%E9%AB%98(%E9%82%84%E5%8E%9F)%40H:ADJ(),%E6%9C%80%E4%BD%8E(%E9%82%84%E5%8E%9F)%40L:ADJ()&d=" + start_date + "," + end_date + "&o=0&t=1&alt=1&area=0A&token=byfrclqxxi4mmvqxb2nfstsc"
    r = requests.get(url)
    d = json.loads(r.text)
    date_list = []
    close_list = []
    data_return = pd.DataFrame(columns=['date', 'close'])
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
    return data_return[::-1].reset_index(drop=True)


# 取得有還原的0050
def _get_high0050_Exdividend(stock_id, start_date, end_date):
    url = "https://datawinner.sysnet.net.tw/data/?s=" + stock_id + "&f=%E6%94%B6%E7%9B%A4(%E9%82%84%E5%8E%9F)%40C:ADJ(),%E9%96%8B%E7%9B%A4(%E9%82%84%E5%8E%9F)%40O:ADJ(),%E6%9C%80%E9%AB%98(%E9%82%84%E5%8E%9F)%40H:ADJ(),%E6%9C%80%E4%BD%8E(%E9%82%84%E5%8E%9F)%40L:ADJ()&d=" + start_date + "," + end_date + "&o=0&t=1&alt=1&area=0A&token=byfrclqxxi4mmvqxb2nfstsc"
    r = requests.get(url)
    d = json.loads(r.text)
    date_list = []
    close_list = []
    high_list = []
    low_list = []
    open_list = []
    data_return = pd.DataFrame(columns=['date', 'highStockclose', 'highStockhigh', 'highStocklow', 'highStockopen'])
    if json.dumps(d["d1"], ensure_ascii=False) != '':
        item_dict = json.loads((json.dumps(d["d1"], ensure_ascii=False)))
        for i in range(0, len(item_dict)):
            close = (json.dumps(item_dict[i]["收盤(還原)"], ensure_ascii=False))
            high = (json.dumps(item_dict[i]["最高(還原)"], ensure_ascii=False))
            low = (json.dumps(item_dict[i]["最低(還原)"], ensure_ascii=False))
            open = (json.dumps(item_dict[i]["開盤(還原)"], ensure_ascii=False))
            date = (json.dumps(item_dict[i]["日期"], ensure_ascii=False)).replace('"', '')
            if close != 'null':
                close_list.append(round(float(close), 2))
                high_list.append(round(float(high), 2))
                low_list.append(round(float(low), 2))
                open_list.append(round(float(open), 2))
                date_list.append(date)
    data_return['highStockclose'] = pd.Series(close_list)
    data_return['highStockhigh'] = pd.Series(high_list)
    data_return['highStocklow'] = pd.Series(low_list)
    data_return['highStockopen'] = pd.Series(open_list)
    data_return['date'] = pd.Series(date_list)
    return data_return[::-1].reset_index(drop=True)

def _get_0050_diff(delay_day, data_return, data_0050_return):
    # 一開始的測試
    # print(data_0050_return.to_string())
    data_return = data_return.merge(data_0050_return, how='left', left_on='date', right_on='date')
    highStcok = 0
    highStcokPrice = 0
    # print(rsv.to_string() )
    print(data_return.to_string())
    sum_list = []
    for i in range(len(data_return)):
        if i + delay_day < len(data_return):
                # print(data_return.iloc[i + delay_day].date)
                if ( round( data_return.iloc[i: i + delay_day].highStockhigh.max() / data_return.iloc[i: i + delay_day].highStocklow.min(), 2)   < 1.10) and (data_return.iloc[i + delay_day + 1].highStockhigh > data_return.iloc[i: i + delay_day].highStockhigh.max()):
                    highStcokPrice = data_return.iloc[i + delay_day + 1].highStockclose
                    print("布林通道縮小，突破向上=" + str(data_return.iloc[i + delay_day + 1].date) + "股價=" + str(
                        data_return.iloc[i + delay_day +1 ].highStockclose))
                    print("損益=" + str(float(data_return.iloc[i + delay_day+ 4 ].highStockclose) - float(highStcokPrice)))
                    sum_list.append(float(data_return.iloc[i + delay_day+ 4].highStockclose) - float(highStcokPrice))
                elif ( round( data_return.iloc[i: i + delay_day].highStockhigh.max() / data_return.iloc[i: i + delay_day].highStocklow.min(), 2)   < 1.10) and (data_return.iloc[i + delay_day + 1].highStocklow < data_return.iloc[i: i + delay_day].highStocklow.min()):
                    highStcokPrice = data_return.iloc[i + delay_day + 1].highStockclose
                    print("布林通道縮小，突破向下=" + str(data_return.iloc[i + delay_day + 1].date) + "股價=" + str(
                        data_return.iloc[i + delay_day + 1 ].highStockclose))
                    print("損益=" + str(  float(highStcokPrice) - float(data_return.iloc[i + delay_day + 4].highStockclose)))
                    sum_list.append(float(highStcokPrice) - float(data_return.iloc[i + delay_day + 4].highStockclose) )
                # elif (i + delay_day == len(data_return) - 1) & highStcok == 1:
                #     print("最後一天，賣進0050日=" + str(data_return.iloc[i + delay_day].date) + "股價=" + str(
                #         data_return.iloc[i + delay_day].highStockclose))
                #     highStcok = 0
                #     print("損益=" + str(float(data_return.iloc[i + delay_day].highStockclose) - float(highStcokPrice)))
                #     sum_list.append(float(data_return.iloc[i + delay_day].highStockclose) - float(highStcokPrice))
    print("總損益=" + str(sum(sum_list)) + ";勝率=" + str(_determine_ratio(sum_list)*100) + ";次數=" + str(len(sum_list)))
    # return sum(sum_list), _determine_ratio(sum_list) * 100

def do_run():
    data_start_date = '20100101'
    data_end_date = '20200618'
    delay_day = 20
    stock_id = "5483"
    # data_return = _get_OTC(data_start_date, data_end_date)
    # data_return = _get_TWSE(data_start_date, data_end_date)
    data_return = _get_high_Exdividend(stock_id, data_start_date, data_end_date)


    data_0050_return = _get_high0050_Exdividend(stock_id, data_start_date, data_end_date)
    sim_return = _get_0050_diff(delay_day, data_return, data_0050_return)


do_run()

