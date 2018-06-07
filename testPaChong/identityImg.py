from PIL import Image
import pytesseract
import urllib.request
import requests
import re
from http import cookiejar
from contextlib import closing
import execjs

s = requests.Session()
# jar = requests.cookies.RequestsCookieJar()


cookie = cookiejar.CookieJar()
urlOpener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))

def getHtml():
    # papg = urlOpener.open('http://ykjcx.yundasys.com/go.php?wen=3839998850701')  # 打开图片的网址
    papg = s.get("http://ykjcx.yundasys.com/go.php?wen=3839999344061")
    # print("cookie==========="+s.cookies.values())
    # html = papg.read()  # 用read方法读成网页源代码，格式为字节对象
    # html = html.decode('gbk')  # 定义编码格式解码字符串(字节转换为字符串)
    # return html
    return papg.text


# 匹配
def getimg(html):
    imgre = re.compile(r' *zb1qBpg2\.php')  # 正则匹配，compile为把正则表达式编译成一个正则表达式对象，提供效率。
    imglist = re.findall(imgre, repr(html))  # 获取字符串中所有匹配的字符串
    for imgurl in imglist:  # 循环图片字符串列表并输出
        # print(imgurl)
        imgUrl = imgurl.replace("src=\\'.", "")
        newImgUrl = "http://ykjcx.yundasys.com/"+imgUrl
        # 下载
        # urllib.request.urlretrieve(url=newImgUrl, filename='C:/img/0.jpg')  # 把图片下载到本地并指定保存目录
        # response = urlOpener.open(newImgUrl).read()
        response = s.get(newImgUrl)
        for t1 in s.cookies.keys():
            print("pre11111==========" + t1)
        # 这里打开一个空的png文件，相当于创建一个空的txt文件,wb表示写文件
        with open('C:/img/0.jpg', 'wb') as file:
             file.write(response.content)  # data相当于一块一块数据写入到我们的图片文件中
        print("下载完成")  # 格式化输出张数

# 匹配
# def getimg():
#     urllib.request.urlretrieve(url="http://ykjcx.yundasys.com/zb1qBpg2.php", filename='C:/img/0.jpg')  # 把图片下载到本地并指定保存目录
#     print("正在下载第%s张" % 55555)  # 格式化输出张数


prehtml=getHtml()
getimg(prehtml)

# 注意eng的版本 这边使用的是3.0版本，不然会报错，在exe文件中新建tessdate文件，把各种语言放进去
code = pytesseract.image_to_string(Image.open("C:/img/0.jpg"), lang="eng", config="-psm 7")
result = eval(code.replace(":", ""))
print(result)


data = {
    "wen": "3839999344061",
    "hh": "23",
    "yzm": result
}

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "zip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    # "Content-Length": "30",
    # "Content-Type": "application/x-www-form-urlencoded",
    # "Cookie": "PHPSESSID=h26utvhc4t6mvnhnsv4purvk71; JSESSIONID=1rC5bGTCDzMGSC3L8D9h6pwJHFvPQCh3J92Pnn9yLcVYMFyp2N0G!1051678070",
    "Host": "ykjcx.yundasys.com",
    "Origin": "http://ykjcx.yundasys.com",
    "Referer": "http://ykjcx.yundasys.com/go.php",
    # "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"
}

value = urllib.parse.urlencode(data).encode('utf-8')
request23 = urllib.request.Request('http://ykjcx.yundasys.com/go_wsd.php')
def getInfoHtml():
    # papg = urlOpener.open(request23, data=value)  # 打开图片的网址
    # s.cookies.clear_session_cookies().set("PHPSESSID", "h26utvhc4t6mvnhnsv4purvk71")
    for t1 in s.cookies.keys():
        print("pre=========="+t1)
    # s.cookies.clear(domain="PHPSESSID")
    # s.cookies.pop("PHPSESSID")
    # s.cookies.set("PHPSESSID", "h26utvhc4t6mvnhnsv4purvk71")
    papg = s.post('http://ykjcx.yundasys.com/go_wsd.php', data=data)
    for t in s.cookies.items():
        print(t)
    # html = papg.read()  # 用read方法读成网页源代码，格式为字节对象
    # html = html.decode('utf-8')  # 定义编码格式解码字符串(字节转换为字符串)
    # return html
    return papg.text

def getValue(html):
    reg = re.compile(r'var g_s=.*;')  # 正则匹配，compile为把正则表达式编译成一个正则表达式对象，提供效率。
    allValue = re.findall(reg, repr(html))  # 获取字符串中所有匹配的字符串
    # keyArr = allValue.split(";")
    keyArr = allValue[0]
    keyValue = keyArr.split(";")
    secretValue= keyValue[0].replace("var g_s=", "")
    # print(keyValue[0].replace("var g_s=", ""))
    return secretValue

def get_js():
    # f = open("D:/WorkSpace/MyWorkSpace/jsdemo/js/des_rsa.js",'r',encoding='UTF-8')
    f = open("yunda.js", 'r', encoding='gb2312')
    line = f.readline()
    htmlstr = ''
    while line:
        htmlstr = htmlstr + line
        line = f.readline()
    return htmlstr

keyHtml = getInfoHtml()
print(keyHtml)
result = getValue(keyHtml)
print(result)

jsstr = get_js()
ctx = execjs.compile(jsstr)
t=ctx.call('allExec', str(result))
print(t)

s.cookies.clear()

# 还未完成要不eval后面的参数穿进去