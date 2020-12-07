from fake_useragent import UserAgent
# startDate = "2019-03-26"
startDate = "2015-01-05"
import time
import random
import requests
import re
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
import time
from bs4 import BeautifulSoup
import pytesseract
from PIL import Image,ImageEnhance
from CODE.LineNotify import lineNotifyMessage
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15"
# proxies = "45.76.52.195:8081"


def _get_ip():
    res = requests.get('https://free-proxy-list.net/')
    m = re.findall('\d+\.\d+\.\d+\.\d+:\d+', res.text)
    validips = []
    for ip in m:
        try:
            res = requests.get('https://api.ipify.org?format=json', proxies={'http': ip, 'https': ip}, timeout=6)
            validips.append(ip)
            # print(res.json())
            # if len(validips) == 2:
            #     break
        except:
            print('FAIL', ip)
    print(validips)
    _write_ip(str(validips) )
    # return validips

def _write_ip(wording):
    # wording = "[{'ip': '35.185.16.35:80'}, {'ip': '217.172.122.2:8080'}, {'ip': '50.235.149.74:8080'}, {'ip': '51.75.147.33:3128'}, {'ip': '36.37.177.186:8080'}, {'ip': '45.76.52.195:8081'}, {'ip': '37.60.18.242:3128'}, {'ip': '193.188.254.67:53281'}, {'ip': '1.10.189.156:32078'}, {'ip': '129.213.187.47:80'}, {'ip': '31.28.99.25:31396'}, {'ip': '83.12.149.202:8080'}, {'ip': '117.58.245.114:40137'}, {'ip': '91.192.2.168:53281'}, {'ip': '188.166.189.185:8080'}, {'ip': '104.198.125.34:3128'}, {'ip': '113.130.126.2:31932'}, {'ip': '1.10.188.202:8080'}, {'ip': '177.244.36.134:8080'}, {'ip': '5.202.188.154:3128'}, {'ip': '51.75.147.43:3128'}, {'ip': '1.10.188.203:45476'}, {'ip': '157.230.103.189:34067'}, {'ip': '220.150.76.85:6000'}, {'ip': '180.183.112.251:3128'}, {'ip': '103.208.152.34:39887'}, {'ip': '212.126.102.142:31785'}]"
    f = open('C:/Users/user/PycharmProjects/untitled2\CODE/common_fumction/ip.txt', 'w')
    f.write(wording)
    f.close()

def _read_ip():
    f = open('C:/Users/user/PycharmProjects/untitled2\CODE/common_fumction/ip.txt')
    k = f.readlines()
    print(k[0])
    # ips_list = eval(str(k) )

    IPs_list = (k[0].split(',') )
    # IPs_list = ( str(k[0]).replace('["','').replace('"]','')  )
    # print(  IPs_list)
    # print(  len(list(IPs_list) ) )
    rad_1int = random.randint(0, len(IPs_list) -1)
    print(  IPs_list[rad_1int].replace('[','').replace(']','').replace("'","") )
    f.close()
    return str(IPs_list[rad_1int].replace('[','').replace(']','').replace("'",""))

def get_chrome_proxy(url):
    # # 三大法人
    # url1 = "https://www.twse.com.tw/fund/T86?response=json&date=20200930&selectType=ALLBUT0999&_=1601879625162"
    # # 各收盤價
    # url2 = "http://www.twse.com.tw/exchangeReport/MI_INDEX?response=json&date=20200929&type=ALLBUT0999&_=1601889071186"
    # # 借券
    # url3 = "http://www.twse.com.tw/exchangeReport/TWT93U?response=json&date=20200929&_=1551965717789"
    try:
        Options.binary_location = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        webdriver_path = 'D:\\chromedriver_win32\\chromedriver.exe'
        options = Options()
        proxies = _read_ip()
        opt = webdriver.ChromeOptions()
        opt.add_argument('--user-agent=%s' % user_agent)
        opt.add_argument('--proxy-server=' + proxies)
        opt.add_argument('--headless')

        driver = webdriver.Chrome(executable_path=webdriver_path, options=opt)
        driver.get(url)  # 前往這個網址
        soup = BeautifulSoup(driver.page_source, "html.parser")
        links = soup.find('pre').getText()
        print(links)
        return links
        driver.close()
    except Exception as exception:
        # print('發生例外錯誤：' +  exception)
        time.sleep(5)
        return get_chrome_proxy(url)

def _get_picture():
    url = 'https://money.cnn.com/data/fear-and-greed/'
    photolimit = 1
    headers = {'User-Agent': 'Mozilla/5.0',
               'Cache-Control' : 'no-cache'}
    response = requests.get(url, headers=headers)  # 使用header避免訪問受到限制
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.find(id="needleChart")['style'].split("url('")[1][:-3]
    folder_path = './'

    print(items)
    html = requests.get(items)  # use 'get' to get photo link path , requests = send request
    img_name = folder_path + str("cnn_fear") + '.png'
    with open(img_name, 'wb') as file:  # 以byte的形式將圖片數據寫入
        file.write(html.content)
        file.flush()
    file.close()  # close file

def _ocr_picture():
    pytesseract.pytesseract.tesseract_cmd = r"D:\Tesseract-OCR\tesseract.exe"
    img = Image.open(r"cnn_fear.png")
    new_img = img.crop((331, 118, 350, 135))  # (left, upper, right, lower)
    img = new_img.resize((int(19 * 3.7), int(17 * 3.7)))
    # new_img = img.crop((0, 0, 350, 135))  # (left, upper, right, lower)
    # print(img.size)
    # img = img.resize((int(615 * 4), int(220 * 4)))

    new_img = ImageEnhance.Contrast(img)
    new_img = new_img.enhance(2.0)
    new_img.show()
    print(pytesseract.image_to_string(new_img))
    message = pytesseract.image_to_string(new_img)
    lineNotifyMessage("目前恐慌指數為" + str(message), 1, 1)
    lineNotifyMessage("目前恐慌指數為" + str(message), 2, 1)
    lineNotifyMessage("目前恐慌指數為" + str(message), 3, 1)
    lineNotifyMessage("目前恐慌指數為" + str(message), 4, 1)

# _ocr_picture()

# _get_picture()


# get_chrome_proxy()

# _get_ip()

# _read_ip()