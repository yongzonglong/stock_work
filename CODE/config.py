from fake_useragent import UserAgent
# startDate = "2019-03-26"
startDate = "2015-01-05"
import time
import random
import requests
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

day_of_week = "mon-sun"
hour = "17"
minute = "00"
second = "00"


twse_html_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Host': 'www.twse.com.tw'}
#
ua = UserAgent()
user_agent = ua.random
rad_2int = random.randint(10, 99)
rad_1int = random.randint(0, 9)

no_cookie_twse_html_headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Host": "www.twse.com.tw",
        "Pragma": "no-cache",
        "Referer": "https://www.twse.com.tw/zh/page/trading/fund/T86.html",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
}

new_twse_html_headers= {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        # "Cookie" :"_ga=GA1.3.1505208941.1512390024; _gid=GA1.3.30770768.1601817947; JSESSIONID=7FEC02DEC3A07A41E943E33E43EE6E1E",
        "Cookie" : "_ga=GA1.3.1505208941.1512390024; _gid=GA1.3.30770768.1601817947; JSESSIONID=C1F06C9F21CEBCE909DCAC73732ED6BB",
        # "Cookie" : "_ga=GA1.3.1505208941.1512390024; _gid=GA1.3.30770768.1601817947; JSESSIONID=E72DFD277F2F3645FEA4169C2A6860EF",
        # "Cookie" : "_ga=GA1.3.1505208941.151239002" + str(rad_1int) +"; _gid=GA1.3.30770768.160181794" + str(rad_1int) + "; JSESSIONID=7FEC02DEC3A07A41E943E33E43EE6E" + str(rad_1int) + "E",
        "Host": "www.twse.com.tw",
        "Pragma": "no-cache",
        "Referer": "https://www.twse.com.tw/zh/page/trading/fund/T86.html",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
        # "User-Agent": user_agent,
        "X-Requested-With": "XMLHttpRequest",
        # "Server": "nginx",
        # "Allow" : "GET, POST, HEAD",
        # "Date" :time.strftime("%Y-%m-%d", time.localtime())
}

