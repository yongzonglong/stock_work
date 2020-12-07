
import requests
import json
from datetime import date
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statistics

def _get_stock_id(url):
    r = requests.get(url)
    d = json.loads(r.text)
    stock_ID_list = []
    if json.dumps(d["d1"], ensure_ascii=False) != '':
        item_dict = json.loads((json.dumps(d["d1"], ensure_ascii=False)))
        for i in range(0, len(item_dict)):
            stock_id = (json.dumps(item_dict[i]["代碼"], ensure_ascii=False))
            stock_ID_list.append(stock_id.replace(".TW", ""))
    # print(stock_id.replace(".TW", ""))
    return stock_ID_list

# 判斷勝率
def _determine_ratio(sum_list):
    ratio = 0
    for i in range(len(sum_list)):
        if sum_list[i] > 1:
            ratio = ratio + 1
    return round(ratio/len(sum_list),3)

def _get_loan_date(stock_id, start_date, end_date):
    url = "https://datawinner.sysnet.net.tw/data/?s=" + stock_id + "&f=MeetlastConYmd&d=" + start_date + "," + end_date +"&o=0&t=1&alt=1&area=0A&token=byfrclqxxi4mmvqxb2nfstsc"
    r = requests.get(url)
    d = json.loads(r.text)
    date_list = []
    loan_date_list = []
    data_return = pd.DataFrame(columns=['date', 'loan_date'])
    if json.dumps(d["d1"], ensure_ascii=False) != '':
        item_dict = json.loads((json.dumps(d["d1"], ensure_ascii=False)))
        for i in range(0, len(item_dict)):
            date = (json.dumps(item_dict[i]["日期"], ensure_ascii=False)).replace('"', '')
            loan_date = (json.dumps(item_dict[i]["融券最後回補日"], ensure_ascii=False))
            if date != 'null':
                date_list.append(date)
                loan_date_list.append(loan_date)
    data_return['date'] = pd.Series(date_list)
    data_return['loan_date'] = pd.Series(loan_date_list)
    return data_return[::-1].reset_index()

def _get_stock_loan_Exdividend(stock_id,  start_date, end_date):
    url = "https://datawinner.sysnet.net.tw/data/?s=" + stock_id + "&f=%E6%94%B6%E7%9B%A4(%E9%82%84%E5%8E%9F)%40C:ADJ(),mVOL,sBalShare,MeetlastConYmd&d=" + start_date + "," + end_date + "&o=0&t=1&alt=1&area=0A&token=byfrclqxxi4mmvqxb2nfstsc"
    r = requests.get(url)
    d = json.loads(r.text)
    close_list = []
    date_list = []
    volume_list = []
    loan_vol_list = []
    data_return = pd.DataFrame(columns=['close', 'date', 'volume', 'loan_vol'])
    if json.dumps(d["d1"], ensure_ascii=False) != '':
        item_dict = json.loads((json.dumps(d["d1"], ensure_ascii=False)))
        for i in range(0, len(item_dict)):
            close = (json.dumps(item_dict[i]["收盤(還原)"], ensure_ascii=False))
            date = (json.dumps(item_dict[i]["日期"], ensure_ascii=False)).replace('"', '')
            volume = (json.dumps(item_dict[i]["成交量(不含鉅額)"], ensure_ascii=False))
            loan_vol = (json.dumps(item_dict[i]["融券餘額張數"], ensure_ascii=False))
            if close != 'null':
                close_list.append(round(float(close), 4))
                date_list.append(date)
                if volume == 'null':
                    print(stock_id + "沒有成交量(不含鉅額)")
                volume_list.append(round(float(volume), 4))
                loan_vol_list.append(loan_vol)
    data_return['close'] = pd.Series(close_list)
    data_return['date'] = pd.Series(date_list)
    data_return['volume'] = pd.Series(volume_list)
    data_return['loan_vol'] = pd.Series(loan_vol_list)
    return data_return[::-1].reset_index()

def _get_ans(stock_id , data_return, loan_date):
    print(data_return.to_string())
    sum_list = []
    for j in range(len(loan_date)):
        for i in range(len(data_return)):
            if (data_return.iloc[i].date == loan_date.iloc[j].loan_date):
                print(loan_date.iloc[j].loan_date)
                if statistics.mean(data_return.iloc[i-6:i-3].volume) < float(data_return.iloc[i-4].loan_vol)*2.5 :
                    # print(data_return.iloc[i-6:i-3].volume)
                    # print(str(float(data_return.iloc[i-4].loan_vol)*2))
                    # print("空暴=" + str(stock_id) + "日期=" + str(loan_date.iloc[j].loan_date))
                    # print(str(float(data_return.iloc[i].close)))
                    # print(str(float(data_return.iloc[i-3].close)))
                    sum_list.append(round( float(data_return.iloc[i].close) / float(data_return.iloc[i-3].close), 2))
    if len(sum_list) > 0 :
        print("總損益=" + str(statistics.mean(sum_list)) + ";勝率=" + str(_determine_ratio(sum_list)))
    data_return = pd.DataFrame(columns=['sum_list'])
    data_return['sum_list'] = pd.Series(sum_list)
    return data_return
if __name__ == '__main__':
    data_start_date = '20160101'
    data_end_date = '20200618'
    stock_id = "5483"
    all_sum_list = []


    data_return = _get_stock_loan_Exdividend(stock_id, data_start_date, data_end_date)
    # print(data_return.to_string())
    loan_date = _get_loan_date(stock_id, data_start_date, data_end_date)
    print(loan_date.to_string())
    _get_ans(stock_id,data_return, loan_date)

    # 取得所有的水泥業
    url_1 = "https://datawinner.sysnet.net.tw/data/?s=G0A101/G0A301/G0A202&f=stk07,stk08&d=TD0&o=0&t=0&alt=1&area=0A&token=byfrclqxxi4mmvqxb2nfstsc"
    # 食品業
    url_2 = "https://datawinner.sysnet.net.tw/data/?s=G0A301/G0A203&f=stk07,stk08,stk11&d=TD0&o=0&t=0&alt=1&area=0A&token=byfrclqxxi4mmvqxb2nfstsc"
    # 塑膠業
    url_3 = "https://datawinner.sysnet.net.tw/data/?s=G0A301/G0A204&f=stk07,stk08,stk11&d=TD0&o=0&t=0&alt=1&area=0A&token=byfrclqxxi4mmvqxb2nfstsc"
    # 紡織業
    url_4 = "https://datawinner.sysnet.net.tw/data/?s=G0A301/G0A205&f=stk07,stk08,stk11&d=TD0&o=0&t=0&alt=1&area=0A&token=byfrclqxxi4mmvqxb2nfstsc"
    # 電機業
    url_5 = "https://datawinner.sysnet.net.tw/data/?s=G0A301/G0A206&f=stk07,stk08,stk11&d=TD0&o=0&t=0&alt=1&area=0A&token=byfrclqxxi4mmvqxb2nfstsc"
    # 電纜業
    url_6 = "https://datawinner.sysnet.net.tw/data/?s=G0A301/G0A207&f=stk07,stk08,stk11&d=TD0&o=0&t=0&alt=1&area=0A&token=byfrclqxxi4mmvqxb2nfstsc"
    # 玻璃業
    url_7 = "https://datawinner.sysnet.net.tw/data/?s=G0A301/G0A208&f=stk07,stk08,stk11&d=TD0&o=0&t=0&alt=1&area=0A&token=byfrclqxxi4mmvqxb2nfstsc"
    # 造紙業
    url_8 = "https://datawinner.sysnet.net.tw/data/?s=G0A301/G0A209&f=stk07,stk08,stk11&d=TD0&o=0&t=0&alt=1&area=0A&token=byfrclqxxi4mmvqxb2nfstsc"
    # 鋼鐵業
    url_9 = "https://datawinner.sysnet.net.tw/data/?s=G0A301/G0A210&f=stk07,stk08,stk11&d=TD0&o=0&t=0&alt=1&area=0A&token=byfrclqxxi4mmvqxb2nfstsc"
    # 橡膠業
    url_10 = "https://datawinner.sysnet.net.tw/data/?s=G0A301/G0A211&f=stk07,stk08,stk11&d=TD0&o=0&t=0&alt=1&area=0A&token=byfrclqxxi4mmvqxb2nfstsc"
    # 汽車業
    url_11 = "https://datawinner.sysnet.net.tw/data/?s=G0A301/G0A212&f=stk07,stk08,stk11&d=TD0&o=0&t=0&alt=1&area=0A&token=byfrclqxxi4mmvqxb2nfstsc"
    # 營建業
    url_12 = "https://datawinner.sysnet.net.tw/data/?s=G0A301/G0A213&f=stk07,stk08,stk11&d=TD0&o=0&t=0&alt=1&area=0A&token=byfrclqxxi4mmvqxb2nfstsc"
    # 航運業
    url_13 = "https://datawinner.sysnet.net.tw/data/?s=G0A301/G0A214&f=stk07,stk08,stk11&d=TD0&o=0&t=0&alt=1&area=0A&token=byfrclqxxi4mmvqxb2nfstsc"
    # 觀光業
    url_14 = "https://datawinner.sysnet.net.tw/data/?s=G0A301/G0A215&f=stk07,stk08,stk11&d=TD0&o=0&t=0&alt=1&area=0A&token=byfrclqxxi4mmvqxb2nfstsc"
    # 金融服務業
    url_15 = "https://datawinner.sysnet.net.tw/data/?s=G0A301/G0A216&f=stk07,stk08,stk11&d=TD0&o=0&t=0&alt=1&area=0A&token=byfrclqxxi4mmvqxb2nfstsc"
    # 百貨業
    url_16 = "https://datawinner.sysnet.net.tw/data/?s=G0A301/G0A217&f=stk07,stk08,stk11&d=TD0&o=0&t=0&alt=1&area=0A&token=byfrclqxxi4mmvqxb2nfstsc"
    # 化工業
    url_17 = "https://datawinner.sysnet.net.tw/data/?s=G0A301/G0A219&f=stk07,stk08,stk11&d=TD0&o=0&t=0&alt=1&area=0A&token=byfrclqxxi4mmvqxb2nfstsc"
    # 生技業
    url_18 = "https://datawinner.sysnet.net.tw/data/?s=G0A301/G0A220&f=stk07,stk08,stk11&d=TD0&o=0&t=0&alt=1&area=0A&token=byfrclqxxi4mmvqxb2nfstsc"
    # 油電業
    url_19 = "https://datawinner.sysnet.net.tw/data/?s=G0A301/G0A221&f=stk07,stk08,stk11&d=TD0&o=0&t=0&alt=1&area=0A&token=byfrclqxxi4mmvqxb2nfstsc"
    # 半導體業
    url_20 = "https://datawinner.sysnet.net.tw/data/?s=G0A301/G0A222&f=stk07,stk08,stk11&d=TD0&o=0&t=0&alt=1&area=0A&token=byfrclqxxi4mmvqxb2nfstsc"
    # 電周邊
    url_21 = "https://datawinner.sysnet.net.tw/data/?s=G0A301/G0A223&f=stk07,stk08,stk11&d=TD0&o=0&t=0&alt=1&area=0A&token=byfrclqxxi4mmvqxb2nfstsc"
    # 光電業
    url_22 = "https://datawinner.sysnet.net.tw/data/?s=G0A301/G0A224&f=stk07,stk08,stk11&d=TD0&o=0&t=0&alt=1&area=0A&token=byfrclqxxi4mmvqxb2nfstsc"
    # 網通業
    url_23 = "https://datawinner.sysnet.net.tw/data/?s=G0A301/G0A225&f=stk07,stk08,stk11&d=TD0&o=0&t=0&alt=1&area=0A&token=byfrclqxxi4mmvqxb2nfstsc"
    # 電零
    url_24 = "https://datawinner.sysnet.net.tw/data/?s=G0A301/G0A226&f=stk07,stk08,stk11&d=TD0&o=0&t=0&alt=1&area=0A&token=byfrclqxxi4mmvqxb2nfstsc"
    # 電通業
    url_25 = "https://datawinner.sysnet.net.tw/data/?s=G0A301/G0A227&f=stk07,stk08,stk11&d=TD0&o=0&t=0&alt=1&area=0A&token=byfrclqxxi4mmvqxb2nfstsc"
    # 資訊業
    url_26 = "https://datawinner.sysnet.net.tw/data/?s=G0A301/G0A228&f=stk07,stk08,stk11&d=TD0&o=0&t=0&alt=1&area=0A&token=byfrclqxxi4mmvqxb2nfstsc"
    # 其它電
    url_27 = "https://datawinner.sysnet.net.tw/data/?s=G0A301/G0A229&f=stk07,stk08,stk11&d=TD0&o=0&t=0&alt=1&area=0A&token=byfrclqxxi4mmvqxb2nfstsc"
    # 文化創意業
    url_28 = "https://datawinner.sysnet.net.tw/data/?s=G0A301/G0A230&f=stk07,stk08,stk11&d=TD0&o=0&t=0&alt=1&area=0A&token=byfrclqxxi4mmvqxb2nfstsc"
    # 農業科技業
    url_29 = "https://datawinner.sysnet.net.tw/data/?s=G0A301/G0A231&f=stk07,stk08,stk11&d=TD0&o=0&t=0&alt=1&area=0A&token=byfrclqxxi4mmvqxb2nfstsc"
    # 電子商務業
    url_30 = "https://datawinner.sysnet.net.tw/data/?s=G0A301/G0A232&f=stk07,stk08,stk11&d=TD0&o=0&t=0&alt=1&area=0A&token=byfrclqxxi4mmvqxb2nfstsc"
    # 所有
    url_31 = "https://datawinner.sysnet.net.tw/data/?s=G0A301&f=stk07,stk08,stk11&d=TD0&o=0&t=0&alt=1&area=0A&token=byfrclqxxi4mmvqxb2nfstsc"
    # stock_ID_list = _get_stock_id(url_23)
    # for i in range(0, len(stock_ID_list)):
    #     loan_date = _get_loan_date(stock_ID_list[i].replace('"', ''), data_start_date, data_end_date)
    #     data_return = _get_stock_loan_Exdividend(stock_ID_list[i].replace('"', ''), data_start_date, data_end_date)
    #
    #     data_return = _get_ans(stock_ID_list[i].replace('"', '') , data_return, loan_date)
    #     all_sum_list.extend(data_return['sum_list'].dropna().tolist())
    # print("總損益 =" + str(statistics.mean(all_sum_list)) + ";勝率=" + str( float(_determine_ratio(all_sum_list)*100)) )
