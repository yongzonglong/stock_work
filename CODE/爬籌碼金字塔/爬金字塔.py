# encoding=UTF-8
import datetime
import requests
import json
import time
import sqlite3
import CODE.config
from bs4 import BeautifulSoup

startDate = CODE.config.startDate
twse_html_headers = CODE.config.twse_html_headers

def do_twse_three_big_price():
    conn = sqlite3.connect('C:/Users/user/Desktop/十大交易人/小胖下載加權指數報酬率Crawler/db/crawler.db')
    c = conn.cursor()
    # time.sleep(5)
    r = requests.get("https://norway.twsthr.info/StockHolders.aspx?stock=5483")
    web_content = r.text
    soup = BeautifulSoup(web_content, 'html.parser')
    trs = soup.find_all('tr', class_="lDS")
    tds = trs[1].find_all('td')
    print trs.__len__()
    print 'date=' + tds[2].text + "num=" + tds[6].text
    # d = json.loads(r.text)
    # print r


def do_big_twse_three_big_price():
    try:
        do_twse_three_big_price()
    except requests.ConnectionError as e:
        print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
        print(str(e))
        time.sleep(30)
        do_big_twse_three_big_price()
    except requests.RequestException as e:
        print("OOPS!! General Error")
        print(str(e))
        time.sleep(30)
        do_big_twse_three_big_price()

do_big_twse_three_big_price()