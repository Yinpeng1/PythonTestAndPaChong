import urllib.request
import urllib.parse
import time


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

# 将字典格式化成能用的形式
data = urllib.parse.urlencode(values).encode('utf-8')

# 这个是百度翻译api的地址
url = 'https://biz.trace.ickd.cn/yd/' + values.get('mailNo') + '?'+data.decode("utf-8")

# 创建一个request,放入我们的地址、数据、头
request23 = urllib.request.Request(url, headers=headers)
# 访问
html = urllib.request.urlopen(request23).read().decode('utf-8')
print(html)


