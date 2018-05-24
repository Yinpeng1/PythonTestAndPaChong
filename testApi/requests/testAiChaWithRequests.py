import time
import requests

# 准备一下头
headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Cookie": "Hm_lvt_39418dcb8e053c84230016438f4ac86c=1526433568; Hm_lpvt_39418dcb8e053c84230016438f4ac86c=1526433568",
    "Host": "biz.trace.ickd.cn",
    "Referer": "https://www.ickd.cn/yd.html",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"
}

time = (time.time())*1000
timeJava = str(time).split(".")[0]
timeJava2 = int(timeJava) + 1
timeJava3 = str(timeJava2)

# 还有我们准备用Post传的值，这里值用字典的形式
values = {
   'mailNo': '3839999344061',
   'tk':'5bbaddce',
   'tm': timeJava,
   'callback': '_jqjsp',
   '_'+timeJava3: ""
}
url = 'https://biz.trace.ickd.cn/yd/' + values.get('mailNo')
request23 = requests.get(url=url, params=values, headers=headers)
# 自动解码
print(request23.text)



