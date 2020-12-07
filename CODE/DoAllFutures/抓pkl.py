# encoding=UTF-8
import datetime
import sqlite3
import math
import requests
import json
import time
import pickle
from pathlib import Path


def load_pkl(file: Path):
    with file.open('rb') as f:
        return pickle.load(f)


# cursor = load_pkl(Path(r"C:/Users/user/Desktop/十大交易人/抓期貨爆單/twntiret_20140101_20191230/twntiret_20140101_20191230.pkl"))

close = load_pkl(Path(r"C:/Users/user/Desktop/十大交易人/抓期貨爆單/twntiret_20140101_20191230/twntiret_20140101_20191230.pkl"))

value = load_pkl(Path(r"C:/Users/user/Desktop/十大交易人/抓期貨爆單/wtx_con_20140101_20191230/wtx_con_20140101_20191230.pkl"))


lastvalue = 0;
date = 0;

for row in value.iterrows():
    if lastvalue == 0:
        lastvalue = row[1].con_net_vol;
    # else:
    #     if (lastvalue -row[1].con_net_vol)>4000:
    #         date = row[1].trade_date
    #         lastclose = 0;
    #         for row2 in close.iterrows():
    #             if lastclose == 0:
    #                 lastclose = row2[1].close;
    #             else:
    #                 if ( math.floor(float(lastclose)) -math.floor(float(row2[1].close)) ) < -40:
    #                     if row2[1].trade_date == date:
    #                         print("做空還大漲", row2[1].trade_date)
    #                 lastclose = row2[1].close;
    #     lastvalue = row[1].con_net_vol;
    else:
        if (lastvalue -row[1].con_net_vol) < -4000:
            date = row[1].trade_date
            lastclose = 0;
            for row2 in close.iterrows():
                if lastclose == 0:
                    lastclose = row2[1].close;
                else:
                    if ( math.floor(float(lastclose)) -math.floor(float(row2[1].close)) ) > 40:
                        if row2[1].trade_date == date:
                            print("做多還大跌", row2[1].trade_date)
                    lastclose = row2[1].close;
        lastvalue = row[1].con_net_vol;









print("Operation done successfully");

