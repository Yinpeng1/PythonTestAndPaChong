from PIL import Image
import pytesseract
import urllib.request
import requests
import re



def getHtml():
    papg = urllib.request.urlopen('http://ykjcx.yundasys.com/go.php?wen=3839999344061')  # 打开图片的网址
    html = papg.read()  # 用read方法读成网页源代码，格式为字节对象
    html = html.decode('gbk')  # 定义编码格式解码字符串(字节转换为字符串)
    return html


# 匹配
def getimg(html):
    imgre = re.compile(r' *zb1qBpg2\.php')  # 正则匹配，compile为把正则表达式编译成一个正则表达式对象，提供效率。
    imglist = re.findall(imgre, repr(html))  # 获取字符串中所有匹配的字符串
    for imgurl in imglist:  # 循环图片字符串列表并输出
        # print(imgurl)
        imgUrl = imgurl.replace("src=\\'.", "")
        newImgUrl = "http://ykjcx.yundasys.com/"+imgUrl
        # 下载
        urllib.request.urlretrieve(url=newImgUrl, filename='C:/img/0.jpg')  # 把图片下载到本地并指定保存目录
        print("下载完成")  # 格式化输出张数

# 匹配
# def getimg():
#     urllib.request.urlretrieve(url="http://ykjcx.yundasys.com/zb1qBpg2.php", filename='C:/img/0.jpg')  # 把图片下载到本地并指定保存目录
#     print("正在下载第%s张" % 55555)  # 格式化输出张数


prehtml=getHtml()
getimg(prehtml)

# 注意eng的版本 这边使用的是3.0版本，不然会报错，在exe文件中新建tessdate文件，把各种语言放进去
code = pytesseract.image_to_string(Image.open("C:/img/0.jpg"), lang="eng", config="-psm 7")
print(eval(code.replace(":", "")))
result = eval(code.replace(":", ""))

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
    "Content-Type": "application/x-www-form-urlencoded",
    "Cookie": "PHPSESSID=h26utvhc4t6mvnhnsv4purvk71; JSESSIONID=1rC5bGTCDzMGSC3L8D9h6pwJHFvPQCh3J92Pnn9yLcVYMFyp2N0G!1051678070",
    "Host": "ykjcx.yundasys.com",
    "Origin": "http://ykjcx.yundasys.com",
    "Referer": "http://ykjcx.yundasys.com/go.php",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"
}

value = urllib.parse.urlencode(data).encode('utf-8')
request23 = urllib.request.Request('http://ykjcx.yundasys.com/go_wsd.php', headers=headers)
def getInfoHtml():
    papg = urllib.request.urlopen(request23, data=value)  # 打开图片的网址
    html = papg.read()  # 用read方法读成网页源代码，格式为字节对象
    html = html.decode('gbk')  # 定义编码格式解码字符串(字节转换为字符串)
    return html

print(getInfoHtml())
# response = requests.post("http://ykjcx.yundasys.com/go_wsd.php", data=result, headers=headers)
# # 自动解码
# print(response.text)
