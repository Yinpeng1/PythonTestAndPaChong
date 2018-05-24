import urllib.request
import urllib.parse
import json
import gzip
import io
import execjs

queryString = input("请输入你想翻译的句子：")
def get_js():
    # f = open("D:/WorkSpace/MyWorkSpace/jsdemo/js/des_rsa.js",'r',encoding='UTF-8')
    f = open("des_rsa.js", 'r', encoding='UTF-8')
    line = f.readline()
    htmlstr = ''
    while line:
        htmlstr = htmlstr + line
        line = f.readline()
    return htmlstr

jsstr = get_js()
ctx = execjs.compile(jsstr)
# print(ctx.call('nihao',content))

# 这个是百度翻译api的地址
url = 'http://fanyi.baidu.com/v2transapi'
# 准备一下头
headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    # "Content-Length": "135",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": "BAIDUID=1F6A837B1730B3CCB9E65C1757365239:FG=1; BIDUPSID=1F6A837B1730B3CCB9E65C1757365239; PSTM=1525403957; "
              "REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1;"
              "H_PS_PSSID=1426_21092_26350_20929; BDSFRCVID=C80sJeC62CrXfR6ApGfjUONONf4hm05TH6aIAcJBFBFLTumcX4keEG0PDf8g0KubMVkPogKK0eOTHk6P; "
              "H_BDCLCKID_SF=tJu8oIt-JIK3fnKkb-nfhPt_qxby26POyeceaJ5nJDoAsj6SKPTNK-LeMbo9WfRwXbvBXxj4QpP-HJ7YKhJ_3J3W-xTDKnIj5IcrKl0MLpbtbb0xynoDX-D0MfnMBMPj5mOnankKLIFKMKtwe5-KjTPW5ptX--Q0aCOasJOOaCv1HInRy4oTj6DDeJ8Ob5JC-ITyof5vBq7Fs-bjDP6-3MvB-fndaboKaHnNXUc-a45RqlbHQft20M0AeMtjBbQaW26r5R7jWhk2eq72y-4-05TXja-qt6DOtJ3fL-08KbnEDRjwMR-_h4L3qxbXq5O-W57Z0l8KttKaJl3wyxQ2y4Fq3tnwWM6JtKoZWJcmWILh8hPmjqr85UAk3-RetxvdBHR4KKJx-4PWeIJo5t5s5n8ehUJiB5O-Ban7BKQxfD_MhKI6e5-aen-W5gTQa4Qj2C_X3b7Ef-nfh-O_bf--D6-gyUvk5fojWD5Q-l7kBhrqsC5bKpQxy550X-b4-lcLHm7-oUbH0RrHeUbHQT3mQhQbbN3i-4ji04DOWb3cWKJq8UbSMTjme6j3ja-DJ5-DfK7QBROo-b5KfRKkb-QK5bt8-q52aI6X56Pssln1-hcqEIL4Ln5ibljBLq3xBtnPB2o92JL22nC2MfbSj4QzLttpL4jG0f7nbCj2hIbo5l5nhMJeb67JDMP0-4cpahOy523ion5vQpnOMxtuD68MDToyjNLs5-70KK3e04oK56rfHtomKPoHK4tJqxT--TnmfnReaJ5nJDoTqxnI06jNKM-EMRo9WfRw5Jn3WCtaQpP-HqTq-U6IQxDzXbOt24JvJI3-Kl0MLpbtbb0xynoDXqKf0MnMBMPj5mOnankKLIcjqR8ZDT8bDTjP; "
              "BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; "
              "from_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D; "
              "PSINO=5; locale=zh; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1526953787,1526954667,1526955278,1526984876; "
              "Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1526984876; to_lang_often=%5B%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D",
    "Host": "fanyi.baidu.com",
    "Origin": "http://fanyi.baidu.com",
    "Referer": "http://fanyi.baidu.com/?aldtype=16047",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}

# 还有我们准备用Post传的值，这里值用字典的形式
values = {
    'from': 'zh',
    'to': 'en',
    'query': queryString,
    'transtype': 'translang',
    'simple_means_flag': '3',
    'sign': ctx.call('nihao', queryString),
    'token': '1dc19b5d66fa4d0e13d2ec22449e268a'
}
# 将字典格式化成能用的形式
data = urllib.parse.urlencode(values).encode('utf-8')
# 创建一个request,放入我们的地址、数据、头
request = urllib.request.Request(url, data, headers)
# 访问
html = urllib.request.urlopen(request)
encoding = html.getheader('Content-Encoding')
content = html.read()
if encoding == 'gzip':
    buf = io.BytesIO(content)
    gf = gzip.GzipFile(fileobj=buf)
    content = gf.read()
print(content)
print(json.loads(content)['trans_result']['data'][0]['dst'])




