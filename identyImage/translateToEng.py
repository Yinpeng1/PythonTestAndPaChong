# !/usr/bin/env python
# -*- coding:utf-8 -*-
from PIL import Image
import pytesseract
from flask_uploads import UploadSet, IMAGES, configure_uploads, ALL
from flask import request, Flask, redirect, url_for, render_template
from testApi import fanyi
import os

app = Flask(__name__)
app.config['UPLOADED_PHOTO_DEST'] = os.path.dirname(os.path.abspath(__file__))
app.config['UPLOADED_PHOTO_ALLOW'] = IMAGES
# def dest(name):
#     return '{}/{}'.format(UPLOAD_DEFAULT_DEST, name)
#app.config['UPLOAD_PHOTO_URL'] = 'http://localhost:5000/'
photos = UploadSet('PHOTO')

configure_uploads(app, photos)

@app.route('/fanyi', methods=['get', 'post'])#router里面第一个参数，是接口的路径
def identyImg():
    filename = photos.save(request.files['file'])
    # 注意eng的版本 这边使用的是3.0版本，不然会报错，在exe文件中新建tessdate文件，把各种语言放进去
    # code = pytesseract.image_to_string(Image.open("C:/img/2.jpg"), lang="chi_sim3")
    code = pytesseract.image_to_string(Image.open(filename), lang="chi_sim3")
    # result = eval(code.replace(":", ""))
    # print(code)
    os.remove(filename)
    s = code.replace("o", "。")
    translateResult = fanyi.translate(s)
    return translateResult

app.run(port=8000, debug=True, host='0.0.0.0')

# if __name__ == '__main__':
#     result = identyImg("")
#     print(result)
    # print(result.encode("utf-8"))
    # translateResult = fanyi.translate(result)
    # print(translateResult)