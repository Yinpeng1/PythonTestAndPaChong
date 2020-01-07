from PIL import Image
import requests
import re
from requests_toolbelt import MultipartEncoder
import random
from urllib.parse import unquote

m = MultipartEncoder({'pic_xxfile': ('2.png', open('2.png', 'rb'), 'image/png')})

proxies = {
    "http":"117.191.11.102:8080"
}

headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
           "Accept-Encoding": "gzip, deflate",
           "Accept-Language": "zh-CN,zh;q=0.9",
           "Cache-Control": "max-age=0",
           "Connection": "keep-alive",
           # "Content-Length": m.content_type.count(),
           "Content-Type": m.content_type,
           "Host": "littlebigluo.qicp.net:47720",
           "Origin": "http://littlebigluo.qicp.net:47720",
           "Referer": "http://littlebigluo.qicp.net:47720/",
           "Upgrade-Insecure-Requests": "1",
           "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
           }

r = requests.post('http://littlebigluo.qicp.net:47720/', data=m, headers=headers)
# r2 = requests.get('http://192.168.0.32:8888/excel/import/ip', proxies=proxies)

# print(r.text)
#
imgre = re.compile(r'<B>(.*?)</B>')
res = re.findall(imgre, repr(r.text))
print(res)

# files = {'file': open("1.png", 'rb')}
# url = 'http://103.46.128.47:47720/'
# request23 = requests.post(url=url, headers=headers, files=files)
# print(request23.request)
# # 自动解码
# # print(request23.text)
# imgre = re.compile(r'<B>(.*?)</B>')
# res = re.findall(imgre, repr(request23.text))
# print(res)
