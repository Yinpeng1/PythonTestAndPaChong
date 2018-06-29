# !/usr/bin/env python
# -*- coding:utf-8 -*-
from PIL import Image
import pytesseract
import flask
from flask import request
# from testApi import fanyi

server = flask.Flask(__name__) #把这个python文件当做一个web服务

@server.route('/fanyi', methods=['get','post'])#router里面第一个参数，是接口的路径
def identyImg():
    # 注意eng的版本 这边使用的是3.0版本，不然会报错，在exe文件中新建tessdate文件，把各种语言放进去
    code = pytesseract.image_to_string(Image.open("C:/img/tn14.png"), lang="fontyp", config="-psm 7")
    # code = pytesseract.image_to_string(Image.open(path), lang="chi_sim3")
    # result = eval(code.replace(":", ""))
    # print(code)
    # s = code.replace("o", "。")
    return code

# server.run(port=8000, host='0.0.0.0')
if __name__ == '__main__':
    result = identyImg()
    print(result)
    # print(result.encode("utf-8"))
    # translateResult = fanyi.translate(result)
    # print(translateResult)