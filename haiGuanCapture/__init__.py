import requests
from PIL import Image
from lxml import etree
import json
from haiGuanCapture.http_client import send_http_post
from flask import Flask, render_template, jsonify, request
import pymysql
import traceback
import random
import base64
import _thread

proxies = {}
ip_cache = []

app = Flask(__name__)
save_image_path = "D:/capture/trans_img/"
url = 'http://ceb2pub.chinaport.gov.cn/limit/outIndex'
url2 = 'https://app.singlewindow.cn/ceb2pubweb/sw/personalAmount'

urlSelect = 'http://ceb2pub.chinaport.gov.cn/limit/outTotalAmount'
urlSelect2 = 'https://app.singlewindow.cn/ceb2pubweb/limit/outTotalAmount'

# urlSelect = 'http://47.101.203.73:8080/product_mapping_check/get/test'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                         '(KHTML,like Gecko) Chrome/55.0.2883.103 Safari/537.36',
           'Connection': 'keep-alive',
           'Host': 'ceb2pub.chinaport.gov.cn',
           'Referer': 'http://ceb2pub.chinaport.gov.cn/limit/outIndex',
           'Origin': 'http://ceb2pub.chinaport.gov.cn'}

headers2 = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            # "Content-Length": "113",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            # "Cookie": "JSESSIONID=3df173d8-6171-4ca6-a2a9-c401d3ef43f9",
            'Host': 'app.singlewindow.cn',
            'Origin': 'https://app.singlewindow.cn',
            'Referer': 'https://app.singlewindow.cn/ceb2pubweb/sw/personalAmount',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36'
}
# 需要给服务端传送的数据，字典格式
data = {}
data2 = {"queryCodeHidden": "cebpub"}

img_byte = ''
img_byte2 = ''

s = requests.session()

connection = pymysql.connect(#host='localhost',
                             # host='172.16.94.212',
                             host='47.98.102.190',
                             user='root',
                             password='123',
                             db='authorize',
                             port=3306,
                             charset='utf8',  # 不能用utf-8
                             cursorclass=pymysql.cursors.DictCursor)

def down_image():
    # ip_result = requests.get(
    #     "http://http.tiqu.alicdns.com/getip3?num=20&type=2&pro=&city=0&yys=0&port=1&pack=39599&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=2&regions=")
    # ip_response = json.loads(ip_result.text)
    # ipList = ip_response["data"]
    # for i in ipList:
    #     ip = i["ip"]
    #     port = i["port"]
    #     ip_port = str(ip) + ":" + str(port)
    #     ip_cache.append(ip_port)
    # proxies["http"] = ip_cache[random.randint(0, len(ip_cache) - 1)]
    # 定义一个session()的对象实体s来储存cookie
    # s.proxies = proxies

    response1 = s.get(url=url, headers=headers)
    response1.encoding = 'utf-8'
    # html1 = response1.text
    html1 = etree.HTML(response1.text)
    # 利用正则表达式找到验证码的url，由于得到的是列表，用list[0]转成str
    cheakcode_url = html1.xpath("//img[@id='verifyCodeImg']/@src")
    response2 = s.get(url=cheakcode_url[0], headers=headers)
    global img_byte
    img_byte = response2
    # 在当前文件夹保存为code.jpg，注意要用'b'的二进制写的方式，用content来获得bytes格式
    with open('code.jpg', 'wb') as fp:
        fp.write(img_byte.content)
    # 打开并显示图片
    # img = Image.open('code.jpg')
    # img.show()

def down_image2():
    response2 = s.get(url=url2, headers=headers2)
    response2.encoding = 'utf-8'
    # html1 = response1.text
    html1 = etree.HTML(response2.text)
    # 利用正则表达式找到验证码的url，由于得到的是列表，用list[0]转成str
    cheakcode_url = html1.xpath("//img[@id='verifyCodeImg']/@src")
    response3 = s.get(url=cheakcode_url[0], headers=headers2)
    global img_byte2
    img_byte2 = response3
    # 在当前文件夹保存为code.jpg，注意要用'b'的二进制写的方式，用content来获得bytes格式
    with open('code.jpg', 'wb') as fp:
        fp.write(img_byte2.content)


def verification_code():
    return send_http_post('code.jpg')


def get_money2(persona_name, id_number):
    down_image2()
    code = verification_code()
    data2['verifyCode'] = code
    data2['personalName'] = base64.b64encode(persona_name.encode('utf-8'))
    data2['idNumber'] = base64.b64encode(id_number.encode('utf-8'))
    data2['sessionKey'] = 'verifyCode'
    data2["queryCodeHidden"] = 'cebpub'
    print(data)
    response3 = s.post(url=urlSelect2, data=data2, headers=headers2)
    print(response3.text)
    json_response = json.loads(response3.text)
    # 识别成功保存图片到指定路径便于以后作为训练集
    with open(str(save_image_path) + str(code) + '.jpg', 'wb') as fp:
        global img_byte2
        fp.write(img_byte2.content)
    if json_response["code"] == '0':
        # 本年度还剩余的可用金额
        money = json_response['result']['innerbalance']
        # 本年度已使用的额度
        already_use = json_response['result']['totalAmount']
        # print("截止目前位置您本年已使用金额:", already_use)
        # print("您本年的可用金额还有:", money)
        return money, already_use
    else:
        # print("验证码错误")
        return 0, 0


def get_money(persona_name, id_number):
    # data['verifyCode'] = input('输入验证码：')
    down_image()
    code = verification_code()
    data['verifyCode'] = code
    data['personalName'] = base64.b64encode(persona_name.encode('utf-8'))
    data['idNumber'] = base64.b64encode(id_number.encode('utf-8'))
    data['sessionKey'] = 'verifyCode'
    print(data)
    response3 = s.post(url=urlSelect, data=data, headers=headers)
    print(response3.text)
    json_response = json.loads(response3.text)
    # 识别成功保存图片到指定路径便于以后作为训练集
    with open(str(save_image_path) + str(code) + '.jpg', 'wb') as fp:
        global img_byte
        fp.write(img_byte.content)
    if json_response["code"] == 10000:
        # 本年度还剩余的可用金额
        money = json_response['result']['innerbalance']
        # 本年度已使用的额度
        already_use = json_response['result']['totalAmount']
        # print("截止目前位置您本年已使用金额:", already_use)
        # print("您本年的可用金额还有:", money)
        return money, already_use
    else:
        # print("验证码错误")
        return 0, 0

@app.route('/api/authorized', methods=['POST'])
def authorized():
    try:
        data = request.get_data()
        j_data = json.loads(data)
        user = j_data["user"]
        ip = j_data["ip"]
        sql = "insert into user_authorize(user, ip)VALUES (%s, %s)"
        with connection.cursor() as cursor:
            cursor.execute(sql, (user, ip))
        connection.commit()
        return jsonify({"code": 1, "errmsg": "授权成功"})
    except Exception as e:
        print("授权错误, 原因:", e)
        return jsonify({"code": 0, "errmsg": "授权错误" + str(e)})


# 校验数据签名
def check_data_sign(user, ip):
    with connection.cursor() as cursor:
        cursor.execute(
            "select * from user_authorize where user = '%s'and ip='%s' and enabled = 1" % (user, ip))
        lists = cursor.fetchall()
        if lists:
            return 1
        else:
            return None

@app.route('/api/get_person_money_limit', methods=['POST'])
def get_person_money_limit():
    try:
        data = request.get_data()
        j_data = json.loads(data)
        persona_name = j_data["persona_name"]
        id_number = j_data["id_number"]
        user = j_data["user"]
        if persona_name is None:
            return jsonify({"code": 0, "errmsg": "缺少参数"})
        if id_number is None:
            return jsonify({"code": 0, "errmsg": "缺少参数"})
        if user is None:
            return jsonify({"code": 0, "errmsg": "缺少参数user"})
        ip = request.remote_addr
        if user == 'im':
            money, already_use = get_money2(persona_name=persona_name, id_number=id_number)
            if money == 0 and already_use == 0:
                return jsonify({"code": 0, "errmsg": "验证码识别错误"})
            return jsonify({"code": 1, "data": {'already_use': already_use, 'left_use': money}})
        # 校验user和ip
        if check_data_sign(user=user, ip=ip):
            pass
        else:
            return jsonify({"code": 0, "errmsg": "未授权用户和ip, 请联系管理员"})
        money, already_use = get_money2(persona_name=persona_name, id_number=id_number)
        return jsonify({"code": 1, "data": {'already_use': already_use, 'left_use': money}})
    except Exception as e:
        print("系统错误, 原因:%s" % e)
        traceback.print_exc(file=open('code_identity.log', 'a+'))
        return jsonify({"code": 0, "errmsg": "内部错误"})


if __name__ == '__main__':
    app.run(host='0.0.0.0')

