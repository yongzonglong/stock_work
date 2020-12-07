import json

from datetime import datetime, timedelta
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.schedulers.blocking import BlockingScheduler
from CODE.ThreeBig_one import do_big_twse_three_big
from CODE.ThreeBig_two import do_big_twse_three_big_price
from CODE.LineNotify import lineNotifyMessage
from CODE.ThreeBigOtc_one import do_big_twse_three_big_OTC
from CODE.ThreeBigOtc_two import do_big_twse_three_big_price_OTC
from CODE.FinFunds.FindTWSE import do_FIND_twse
from CODE.FinFunds.FindOTC import do_FIND_otc
from SecurityLending.SecurityLending_one import do_twse_securitylending_num
from SecurityLending.SecurityLending_two import do_twse_securitylending_num_price
from SecurityLending.FindBack import find_back
from SecurityLending.FindSell import find_sell
from CODE.DoAllFutures.DoAllFurtrues_1 import  do_AllFurtrues
from CODE.DoAllFutures.DoAllFurtrues_2 import do_AllFurtrues_price
from CODE.DoAllFutures.DoAllFurtrues_3 import DownloadOption_Call
from CODE.DoAllFutures.DoAllFurtrues_4 import DownloadOption_Put
from CODE.DoAllFutures.FindAllFutures import Find_AllFurtrues
from CODE.FindSelf.FindSelfTWSE import do_SELF_twse
from CODE.FindSelf.FindSelfOTC import do_SELF_otc
from CODE.Macroeconomics.DownloadUSD import Download_USD
from CODE.Macroeconomics.DownloadPredit import Download_Predict
from CODE.Find_0056_.calculate_0056_lowhigh import calculate_0056_lowhith_run
from CODE.Find_0056_.calculate_OTC_lowhigh import calculact_OTC_lowhigh_run
from CODE.common_fumction.commom_proxy_ip import _get_ip, _get_picture, _ocr_picture
import CODE.config


def run():
    scheduler = BlockingScheduler()
    # 排程
    trigger0 = CronTrigger(day_of_week=CODE.config.day_of_week, hour=8,
                          minute=59, second=00)
    trigger0a = CronTrigger(day_of_week=CODE.config.day_of_week, hour=13,
                          minute=29, second=00)
    trigger0b = CronTrigger(day_of_week=CODE.config.day_of_week, hour=8,
                          minute=30, second=00)
    trigger0c = CronTrigger(day_of_week=CODE.config.day_of_week, hour=8,
                          minute=58, second=00)
    # scheduler.add_job(func=lineNotifyMessage, trigger=trigger0, args=["準備開盤囉~~", 2],misfire_grace_time=30)
    # scheduler.add_job(func=lineNotifyMessage, trigger=trigger0a, args=["準備收盤囉~~", 2],misfire_grace_time=30)
    scheduler.add_job(func=_get_picture, trigger=trigger0b, args=[], misfire_grace_time=30)
    scheduler.add_job(func=_get_picture, trigger=trigger0c, args=[], misfire_grace_time=30)
    scheduler.add_job(func=_ocr_picture, trigger=trigger0, args=[], misfire_grace_time=30)

    scheduler.add_job(func=_get_ip, trigger=trigger0a, args=[],misfire_grace_time=30)

    # 爬證交所
    # 下午四點15 6分開始爬證交所
    trigger = CronTrigger(day_of_week=CODE.config.day_of_week, hour=16,
                          minute=10, second=00)
    trigger2 = CronTrigger(day_of_week=CODE.config.day_of_week, hour=16,
                          minute=30, second=00)
    trigger3 = CronTrigger(day_of_week=CODE.config.day_of_week, hour=16,
                          minute=40, second=00)
    trigger3a = CronTrigger(day_of_week=CODE.config.day_of_week, hour=16,
                          minute=40, second=00)
    scheduler.add_job(func=do_big_twse_three_big, trigger=trigger, args=[0,1],
                      misfire_grace_time=30)
    scheduler.add_job(func=do_big_twse_three_big_price, trigger=trigger2, args=[0,1],
                      misfire_grace_time=30)
    scheduler.add_job(func=do_FIND_twse, trigger=trigger3, args=[],
                      misfire_grace_time=30)
    scheduler.add_job(func=do_SELF_twse, trigger=trigger3a, args=[],
                      misfire_grace_time=30)

    # 爬櫃買中心
    # 下午三點5 6分開始爬櫃買
    trigger4 = CronTrigger(day_of_week=CODE.config.day_of_week, hour=17,
                          minute=15, second=00)
    trigger5 = CronTrigger(day_of_week=CODE.config.day_of_week, hour=17,
                          minute=16, second=00)
    trigger6 = CronTrigger(day_of_week=CODE.config.day_of_week, hour=17,
                          minute=17, second=00)
    trigger6a = CronTrigger(day_of_week=CODE.config.day_of_week, hour=17,
                          minute=18, second=00)
    scheduler.add_job(func=do_big_twse_three_big_OTC, trigger=trigger4, args=[0,1],
                      misfire_grace_time=30)
    scheduler.add_job(func=do_big_twse_three_big_price_OTC, trigger=trigger5, args=[0,1],
                      misfire_grace_time=30)
    scheduler.add_job(func=do_FIND_otc, trigger=trigger6, args=[],
                      misfire_grace_time=30)
    scheduler.add_job(func=do_SELF_otc, trigger=trigger6a, args=[],
                      misfire_grace_time=30)

    # 爬借券賣出
    trigger7 = CronTrigger(day_of_week=CODE.config.day_of_week, hour=22,
                          minute=15, second=00)
    trigger8 = CronTrigger(day_of_week=CODE.config.day_of_week, hour=22,
                          minute=35, second=00)
    trigger9 = CronTrigger(day_of_week=CODE.config.day_of_week, hour=22,
                          minute=58, second=00)
    trigger10 = CronTrigger(day_of_week=CODE.config.day_of_week, hour=22,
                          minute=59, second=00)
    scheduler.add_job(func=do_twse_securitylending_num, trigger=trigger7, args=[0,1],
                      misfire_grace_time=30)
    scheduler.add_job(func=do_twse_securitylending_num_price, trigger=trigger8, args=[0,1],
                      misfire_grace_time=30)

    scheduler.add_job(func=find_back, trigger=trigger9, args=[0],misfire_grace_time=30)
    scheduler.add_job(func=find_sell, trigger=trigger10, args=[0],misfire_grace_time=30)

    # 爬外資期貨十大交易人
    trigger11 = CronTrigger(day_of_week=CODE.config.day_of_week, hour=18,
                          minute=20, second=00)
    trigger12 = CronTrigger(day_of_week=CODE.config.day_of_week, hour=18,
                          minute=21, second=00)
    trigger13 = CronTrigger(day_of_week=CODE.config.day_of_week, hour=18,
                          minute=22, second=00)
    trigger14 = CronTrigger(day_of_week=CODE.config.day_of_week, hour=18,
                          minute=23, second=00)
    trigger15 = CronTrigger(day_of_week=CODE.config.day_of_week, hour=18,
                          minute=30, second=00)
    scheduler.add_job(func=do_AllFurtrues, trigger=trigger11, args=[0,1],
                      misfire_grace_time=30)
    scheduler.add_job(func=do_AllFurtrues_price, trigger=trigger12, args=[0,1],
                      misfire_grace_time=30)
    scheduler.add_job(func=DownloadOption_Call, trigger=trigger13, args=[0,1],
                      misfire_grace_time=30)
    scheduler.add_job(func=DownloadOption_Put, trigger=trigger14, args=[0,1],
                      misfire_grace_time=30)
    scheduler.add_job(func=Find_AllFurtrues, trigger=trigger15, args=[0],
                      misfire_grace_time=30)

    # 爬整體經濟
    trigger16 = CronTrigger(day_of_week=CODE.config.day_of_week, hour=12,
                          minute=25, second=00)
    trigger17 = CronTrigger(day_of_week=CODE.config.day_of_week, hour=22,
                          minute=26, second=00)
    scheduler.add_job(func=Download_USD, trigger=trigger16, args=[0,1],
                      misfire_grace_time=30)
    # scheduler.add_job(func=Download_Predict, trigger=trigger17, args=[1],
    #                   misfire_grace_time=30)

    #爬通知目前0056和櫃買的分位數
    trigger18 = CronTrigger(day_of_week=CODE.config.day_of_week, hour=21,
                            minute=47, second=00)
    trigger19 = CronTrigger(day_of_week=CODE.config.day_of_week, hour=21,
                            minute=50, second=00)
    scheduler.add_job(func=calculate_0056_lowhith_run, trigger=trigger18, args=[0],misfire_grace_time=30)
    # scheduler.add_job(func=calculact_OTC_lowhigh_run, trigger=trigger19, args=[0],misfire_grace_time=30)


    scheduler.start()
run()