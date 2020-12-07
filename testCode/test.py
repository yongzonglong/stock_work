import requests
# from selenium import webdriver

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3573.0 Safari/537.36'
    }

host = "https://www.twse.com.tw"
url1 = host + "/zh/page/trading/fund/T86.html"
r = requests.get(url1, headers= headers)
token = r.cookies.items()[0][1]
print(token)
daytime = "20200929"
# url2 = "http://www.twse.com.tw/exchangeReport/MI_INDEX?response=json&date=" + daytime + "&type=ALLBUT0999&_=1601830606137"
# headers = {
# "token": token,
# "Host": "10.70.18.33:8083",
# "User-Agent": " Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:46.0) Gecko/20100101 Firefox/46.0",
# "Accept": "application/json, text/javascript, */*; q=0.01",
# "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
# "Accept-Encoding": "gzip, deflate",
# "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
# "X-Requested-With": "XMLHttpRequest",
# "Connection": "keep-alive",
# "Content-Length": "18",
# "charset": "UTF-8",
# "cookie": "token=" + token
# }
#
#
# print(s.status_code, s.text)
