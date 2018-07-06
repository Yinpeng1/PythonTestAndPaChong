import requests
import re

# 准备一下头
headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Cookie": "Hm_lvt_39418dcb8e053c84230016438f4ac86c=1526433568; Hm_lpvt_39418dcb8e053c84230016438f4ac86c=1526433568",
    "Host": "biz.trace.ickd.cn",
    "Referer": "http://103.46.128.47:47720/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"
}

# 还有我们准备用Post传的值，这里值用字典的形式
values = {

}
# files = {'file': open("C:\\img\\123.jpg", 'rb')}
# url = 'http://103.46.128.47:47720/'
# request23 = requests.post(url=url, headers=headers, files=files)
# 自动解码
# print(request23.text)
requests = '<br><img src=/upload/2018-07-06-14-59-20_1159_123.jpg><p>经过仔细揣摩-图片貌似选:    <font color="red"><font size="+2"><B>2 7</B></font></font></p><p><font size="1">第一排图片从左到右编号依次为:1 2 3 4</font></p><p><font size="1">第二排图片从左到右编号依次为:5 6 7 8</font></p><p><font size="1">耗时:461毫秒!觉得俺bigluo眼力如何??</font></p><p><font size="1">如果不确定结果是否正确，不妨登陆一下12306试试！！</font></p><p><font size="1">有意见或建议？？欢迎交流:3490699170@qq.com</font></p>'
imgre = re.compile(r'<B>(.*?)</B>')
res = re.findall(imgre, repr(requests))
for i in res:
    arr = str(i).split(" ")
    for j in arr:
        print(j)
# print(res)





