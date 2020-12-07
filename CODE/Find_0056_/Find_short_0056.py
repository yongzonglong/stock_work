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

# 取得加權指數
def _get_TWSE( start_date, end_date):
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
                close_list.append( round(  float (close) ))
                date_list.append(date)
    data_return['close'] = pd.Series(close_list)
    data_return['date'] = pd.Series(date_list)
    return data_return[::-1].reset_index()

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
                close_list.append( round(  float (close),2 ))
                date_list.append(date)
    data_return['close'] = pd.Series(close_list)
    data_return['date'] = pd.Series(date_list)
    return data_return[::-1].reset_index()


# 取得有還原的0056
def _get_high_Exdividend( start_date, end_date):
    url = "https://datawinner.sysnet.net.tw/data/?s=0056&f=%E6%94%B6%E7%9B%A4(%E9%82%84%E5%8E%9F)%40C:ADJ()&d=" + start_date + "," + end_date + "&o=0&t=0&alt=1&area=0A&token=byfrclqxxi4mmvqxb2nfstsc"
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
                close_list.append( round(  float (close),2 ))
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
                close_list.append( round(  float (close),2 ))
                date_list.append(date)
    data_return['highStockclose'] = pd.Series(close_list)
    data_return['date'] = pd.Series(date_list)
    return data_return[::-1].reset_index()

def _get_0056_diff(lowTh, upTh,data_return,data_0056_return, delay_day):

    data_return = data_return.merge(data_0056_return, left_on='date', right_on='date')
    highStcok = 0
    highStcokPrice = 0
    # delay_day = 90
    sum_list=[]
    for i in range(len(data_return)):
        if i+delay_day < len(data_return):
            if ( data_return.iloc[i+delay_day].close > np.percentile(data_return.iloc[i:i + delay_day-1].close, (lowTh), interpolation='midpoint') )& ( highStcok == 0 ):
                highStcok = -1
                highStcokPrice = data_return.iloc[i+delay_day].highStockclose
                # print("做空0056日=" + data_return.iloc[i+delay_day].date + "股價=" + data_return.iloc[i+delay_day].highStockclose )
            elif ( data_return.iloc[i + delay_day].close < np.percentile(data_return.iloc[i:i + delay_day-1].close, (upTh),interpolation='midpoint') )& ( highStcok == -1 ):
                highStcok = 0
                # print("回補0056日=" + data_return.iloc[i + delay_day].date + "股價=" + data_return.iloc[i+delay_day].highStockclose )
                # print("損益=" + str( float(highStcokPrice) - float(data_return.iloc[i+delay_day].highStockclose) ) )
                sum_list.append( float(highStcokPrice) - float(data_return.iloc[i+delay_day].highStockclose)    )
            elif (i + delay_day == len(data_return)-1 ) & highStcok == -1:
                # print("最後一天，回補0056日=" + data_return.iloc[i + delay_day].date + "股價=" + data_return.iloc[i + delay_day].highStockclose)
                highStcok = 0
                # print("損益=" + str( float(highStcokPrice) - float(data_return.iloc[i+delay_day].highStockclose)) )
                sum_list.append( float(highStcokPrice) - float(data_return.iloc[i+delay_day].highStockclose)    )
    # print(sum_list)
    # print( sum(sum_list)  )
    # print("總損益=" + str( sum(sum_list) ) + ";勝率=" + str(_determine_ratio(sum_list) ) )
    return sum_list
if __name__ == '__main__':
    start_date = '20150101'
    end_date = '20200505'
    # data_return = _get_OTC(start_date, end_date)
    data_return = _get_TWSE(start_date, end_date)
    # data_return = _get_high(start_date, end_date)
    # data_return = _get_high_Exdividend(start_date, end_date)


    # data_0056_return = _get_high0056(start_date, end_date)
    # 還原0056的除息
    data_0056_return = _get_high0056_Exdividend(start_date, end_date)

    # _get_0056_diff(100, 35, data_return, data_0056_return,80)



    for delay_day in range(40,251,10):
        print("delay_day=" + str(delay_day))
        all_ratio = pd.DataFrame()
        all_sum = []
        win_ratio = []
        index = []
        for i in range(0,101,5):
            for j in range(0,i+1,5):
                sum_lists = _get_0056_diff(i,j,data_return,data_0056_return, delay_day)
                index.append( str(i) + ',' + str(j) )
                all_sum.append( sum(sum_lists) )
                win_ratio.append(_determine_ratio(sum_lists) )
        all_ratio['index'] = pd.Series(index)
        all_ratio['win_ratio'] = pd.Series(win_ratio)
        all_ratio['all_sum'] = pd.Series(all_sum)
        # for i in range(len(all_ratio)):
        print(all_ratio.sort_values(by='all_sum').to_string())

    # ax = plt.subplot(projection='3d')  # 创建一个三维的绘图工程
    # ax.scatter(x, y, z, c='r')  # 绘制数据点,颜色是红色
    # ax.set_zlabel('總和')  # 坐标轴
    # ax.set_ylabel('上分位數')
    # ax.set_xlabel('下分位數')
    # plt.draw()
    # plt.pause(10)
    # plt.savefig('3D.jpg')
    # plt.close()


