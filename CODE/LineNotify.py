import requests
import CODE.config
from bs4 import BeautifulSoup

def lineNotifyMessage(msg, index, picture = 2):
    # 修改為你的權杖內容
    if index == 1:
        token = 'LzHoJYdU265o0VnXcSNclhKa5ABu280T3Kka0m4Qzyh'
    elif index == 2:
        token = '0alEaZdQ4BMf4LfeE60241QVW3bTX7q7L86DfP61R64'
    elif index == 3:
        token = "fK2J4OBrl30JSYItRzckfpvgammz5SQcOlJQDzEsek9"
     # 期貨測試小組
    elif index == 4:
        token = "pxYiD218ziaUbMk4KOgg9MM9al5SXebelYkvud2zxIL"
    payload = {'message': msg}
    if picture == 1:
        picURI = "./common_fumction/cnn_fear.png"
        files = {'imageFile': open(picURI, 'rb')}
        headers = {
            "Authorization": "Bearer " + token,
        }
        r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload, files  = files )
        print(r.text)
    else:
        headers = {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload)
    return r.status_code


# 修改為你要傳送的訊息內容
message = '恐慌指數來囉~~'


# lineNotifyMessage(message, 2,1)
# lineNotifyMessage(message, 3, 1)
