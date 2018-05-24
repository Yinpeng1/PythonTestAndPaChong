import urllib.request
import urllib.parse
import time

# 这个是百度翻译api的地址
url = 'https://biz.trace.ickd.cn/yd/3839999344061'
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
# 创建一个request,放入我们的地址、数据、头
request = urllib.request.Request(url, headers)
# 访问
html = urllib.request.urlopen(request, data).read().decode('utf-8')
# data1 = gzip.decompress(html).decode("utf-8")
# 利用json解析包解析返回的json数据 拿到翻译结果
# print(json.loads(html)['trans_result']['data'][0]['dst'])
print(html)
# print(gzip.decompress(data1.query).decode("utf-8"))


