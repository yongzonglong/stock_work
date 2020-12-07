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


# 取得加權指數
def _get_TWSE(start_date, end_date):
    url = "https://datawinner.sysnet.net.tw/data/?s=TWNT0000&f=C&d=" + start_date + "," + end_date + "&o=0&t=0&alt=1&area=0A&token=byfrclqxxi4mmvqxb2nfstsc"
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
                close_list.append(round(float(close), 2))
                date_list.append(date)
    data_return['close'] = pd.Series(close_list)
    data_return['date'] = pd.Series(date_list)
    return data_return[::-1].reset_index(drop=True)


# 取得櫃買指數
def _get_OTC(start_date, end_date):
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
                close_list.append(round(float(close), 2))
                date_list.append(date)
    data_return['close'] = pd.Series(close_list)
    data_return['date'] = pd.Series(date_list)
    return data_return[::-1].reset_index(drop=True)


# 取得有還原的0050
def _get_high_Exdividend(start_date, end_date):
    url = "https://datawinner.sysnet.net.tw/data/?s=0050&f=%E6%94%B6%E7%9B%A4(%E9%82%84%E5%8E%9F)%40C:ADJ(),%E9%96%8B%E7%9B%A4(%E9%82%84%E5%8E%9F)%40O:ADJ(),%E6%9C%80%E9%AB%98(%E9%82%84%E5%8E%9F)%40H:ADJ(),%E6%9C%80%E4%BD%8E(%E9%82%84%E5%8E%9F)%40L:ADJ()&d=" + start_date + "," + end_date + "&o=0&t=1&alt=1&area=0A&token=byfrclqxxi4mmvqxb2nfstsc"
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
def _get_high0050_Exdividend(start_date, end_date):
    url = "https://datawinner.sysnet.net.tw/data/?s=0050&f=%E6%94%B6%E7%9B%A4(%E9%82%84%E5%8E%9F)%40C:ADJ(),%E9%96%8B%E7%9B%A4(%E9%82%84%E5%8E%9F)%40O:ADJ(),%E6%9C%80%E9%AB%98(%E9%82%84%E5%8E%9F)%40H:ADJ(),%E6%9C%80%E4%BD%8E(%E9%82%84%E5%8E%9F)%40L:ADJ()&d=" + start_date + "," + end_date + "&o=0&t=1&alt=1&area=0A&token=byfrclqxxi4mmvqxb2nfstsc"
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

def _get_rsv(data_return, delay_day):
    rsv = (data_return['highStockclose'] - data_return['highStocklow'].rolling(window=delay_day).min()) / (
                data_return['highStockhigh'].rolling(window=delay_day).max() - data_return['highStocklow'].rolling(
            window=delay_day).min()) * 100
    # 把前8筆NaN改為0
    rsv = np.nan_to_num(rsv)
    # 資料放入dataframe裡
    RSV = pd.DataFrame(rsv)
    # 名稱定義為RSV
    RSV.columns = ['RSV']
    # 索引比照收盤價以日期為主
    RSV.index = data_return['close'].index
    return RSV['RSV']

def _get_kd(data_return, delay_day):
    # 創建K值
    k1 = []
    # a = 74.02
    for a in range(delay_day-1):
        a = 74.02
        k1.append(a)
    k1 = pd.DataFrame(k1)
    k1.columns = ['K']
    print(k1)
    k2 = []
    k_temp = a
    for i in range(len(data_return) - delay_day + 1):
        # 當日K值=前一日K值 * 2/3 + 當日RSV * 1/3
        k_temp = k_temp * 2 / 3 + data_return['RSV'][i + delay_day -1] * (1 / 3)
        k2.append(k_temp)
    k2 = pd.DataFrame(k2)
    k2.columns = ['K']
    K = pd.concat([k1, k2])
    K.index = data_return['close'].index
    data_return['K'] = K['K']
    return data_return

def _get_d(data_return, delay_day):
    d1 = []
    for b in range(delay_day -1):
        b = 81.58
        d1.append(b)
    d1 = pd.DataFrame(d1)
    d1.columns = ['D']
    d2 = []
    d_temp = b
    for j in range(len(data_return) - delay_day + 1):
        # 當日D值=前一日D值 * 2/3 + 當日K值 * 1/3
        d_temp = d_temp * 2 / 3 + data_return['K'][j + delay_day - 1] * (1 / 3)
        d2.append(d_temp)
    d2 = pd.DataFrame(d2)
    d2.columns = ['D']
    D = pd.concat([d1, d2])
    D.index = data_return['close'].index
    data_return['D'] = D['D']
    return data_return

def _get_0050_diff(lowTh, upTh, data_return, data_0050_return, delay_day, buy_start_date):
    # 一開始的測試
    # print(data_0050_return.to_string())
    data_return = data_return.merge(data_0050_return, how='left', left_on='date', right_on='date')
    highStcok = 0
    highStcokPrice = 0
    data_return['RSV'] = _get_rsv(data_return, delay_day)
    # print(rsv.to_string() )
    data_return = _get_kd(data_return,delay_day)
    data_return = _get_d(data_return,delay_day)
    print(data_return.to_string())
    sum_list = []
    for i in range(len(data_return)):
        if i + delay_day < len(data_return):
            if (data_return.iloc[i + delay_day].date >= buy_start_date) :
                # print(data_return.iloc[i + delay_day].date)
                if (data_return.iloc[i + delay_day].K < lowTh) & ( highStcok == 0):
                    highStcok = 1
                    highStcokPrice = data_return.iloc[i + delay_day].highStockclose
                    print("買進0050日=" + str(data_return.iloc[i + delay_day].date) + "股價=" + str(
                        data_return.iloc[i + delay_day].highStockclose))
                    # 計算 9 日內最高成交價
                elif (data_return.iloc[i + delay_day].K > upTh) & (highStcok == 1):
                    highStcok = 0
                    print("賣進0050日=" + str(data_return.iloc[i + delay_day].date) + "股價=" + str(
                        data_return.iloc[i + delay_day].highStockclose))
                    print("損益=" + str(float(data_return.iloc[i + delay_day].highStockclose) - float(highStcokPrice)))
                    sum_list.append(float(data_return.iloc[i + delay_day].highStockclose) - float(highStcokPrice))
                elif (i + delay_day == len(data_return) - 1) & highStcok == 1:
                    print("最後一天，賣進0050日=" + str(data_return.iloc[i + delay_day].date) + "股價=" + str(
                        data_return.iloc[i + delay_day].highStockclose))
                    highStcok = 0
                    print("損益=" + str(float(data_return.iloc[i + delay_day].highStockclose) - float(highStcokPrice)))
                    sum_list.append(float(data_return.iloc[i + delay_day].highStockclose) - float(highStcokPrice))
    print("總損益=" + str(sum(sum_list)) + ";勝率=" + str(_determine_ratio(sum_list)))
    # return sum(sum_list), _determine_ratio(sum_list) * 100

def do_run(lowTh, upTh, delay_day):
    data_start_date = '20090101'
    data_end_date = '20200618'
    buy_start_date = '20100101'
    # delay_day = 190
    # data_return = _get_OTC(data_start_date, data_end_date)
    # data_return = _get_TWSE(data_start_date, data_end_date)
    data_return = _get_high_Exdividend(data_start_date, data_end_date)
    # 還原0050的除息
    data_0050_return = _get_high0050_Exdividend(data_start_date, data_end_date)
    sim_return = _get_0050_diff(lowTh, upTh, data_return, data_0050_return, delay_day, buy_start_date)
    # mypath = r"C:\Users\F62Q\Desktop\AI\result"
    # parameter = TRADE_PARMETER(
    #     # funds=120000000,
    #     # per_trade_limit=1000000,
    #     # funds=53000000,
    #     funds=1000000,
    #     per_trade_limit=None,
    #     date_start=min(sim_return.ymdOn),
    #     date_end=max(sim_return.ymdOn),
    #     # continue_bs=True,
    #     stop_win=None,
    #     stop_loss=None,
    #     mov_win=None,
    #     mov_win_startup=None,
    #     max_sym_trans=1,
    #     charge_discount=0.6,
    #     trade_mode=TradeMode.BUY_ONLY,
    #     file_path= os.path.join(mypath, str(lowTh) + "-" + str(upTh) )
    # )
    # do_trans(sim_return, parameter, allow_no_money=True)
if __name__ == '__main__':
    delay_day = 9
    do_run(20, 80, delay_day)

    # profit, win_rate = _get_0056_diff(65, 90, data_return, data_0056_return, 150)
    # records = []
    # with futures.ProcessPoolExecutor(max_workers=os.cpu_count() - 1) as executor:
    #     tasks = {}
    #     for in_p, out_p, days in product(range(0, 101, 5), range(0, 101, 5), range(40, 241, 5)):
    #         if in_p > out_p:
    #             continue
    #         f = executor.submit(_get_0056_diff, in_p, out_p, days)
        #     tasks[f] = f"{in_p}_{out_p}_{days}"
        #
        # for f in tqdm(futures.as_completed(tasks), ascii=True, total=len(tasks)):
        #     profit, win_rate = f.result()
        #     in_p, out_p, days = tasks[f].split('_')
        #
        #     records.append((in_p, out_p, days, profit, win_rate))

    # result_df = pd.DataFrame(records, columns=['in_p', 'out_p', 'days', 'profit', 'win_rate'])
    # result_df = result_df.sort_values(by=['in_p', 'out_p', 'days']).reset_index(drop=True)
    # result_df.to_csv('0056.csv',index=False)
    # print(result_df)


