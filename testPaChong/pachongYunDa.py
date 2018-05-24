import urllib.request
import re
import requests
from contextlib import closing

def getHtml():
    papg = urllib.request.urlopen('http://ykjcx.yundasys.com/go.php?wen=3839999344061')  # 打开图片的网址
    html = papg.read()  # 用read方法读成网页源代码，格式为字节对象
    html = html.decode('gbk')  # 定义编码格式解码字符串(字节转换为字符串)
    return html


# 匹配
def getimg(html):
    imgre = re.compile(r' *zb1qBpg2\.php')  # 正则匹配，compile为把正则表达式编译成一个正则表达式对象，提供效率。
    imglist = re.findall(imgre, repr(html))  # 获取字符串中所有匹配的字符串
    x = 0  # 定义全局变量默认为0
    for imgurl in imglist:  # 循环图片字符串列表并输出
        # print(imgurl)
        imgUrl = imgurl.replace("src=\\'.", "")
        newImgUrl = "http://ykjcx.yundasys.com/"+imgUrl
        # print("http://ykjcx.yundasys.com/"+newImgUrl)
        # 下载
        urllib.request.urlretrieve(url=newImgUrl, filename='C:/img/%s.jpg' % x)  # 把图片下载到本地并指定保存目录
        x += 1  # 每次自增1
        print("正在下载第%s张" % x)  # 格式化输出张数


# 匹配
# def getimg():
#     urllib.request.urlretrieve(url="http://ykjcx.yundasys.com/zb1qBpg2.php", filename='C:/img/hello1.jpg')  # 把图片下载到本地并指定保存目录
#     print("正在下载第%s张" % 55555)  # 格式化输出张数


# def getPhp(url):
#     response = requests.get(url, stream=True)
#     with closing(requests.get(url, stream=True)) as response:
#         # 这里打开一个空的png文件，相当于创建一个空的txt文件,wb表示写文件
#         with open('C:/img/nihao.jpg', 'wb') as file:
#             # 每128个流遍历一次
#              for data in response.iter_content(128):
#                  # 把流写入到文件，这个文件最后写入完成就是，selenium.png
#                  file.write(data)  # data相当于一块一块数据写入到我们的图片文件中
#     print(response.status_code)


# 调用函数
html = getHtml()
print(getimg(html))
# getPhp("http://ykjcx.yundasys.com/zb1qBpg2.php")

# print(getimg(html))
