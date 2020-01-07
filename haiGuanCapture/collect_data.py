# -*- coding: utf-8 -*-
import requests
from lxml import etree
from flask import Flask, render_template, jsonify, request
import json

wayNum = 1710542540

post_url = "https://apps.dhl.com.hk/eng_fi/eng_fi_Result.jsp"

hearers={
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Content-Length": "33",
    "Content-Type": "application/x-www-form-urlencoded",
    "Host": "apps.dhl.com.hk",
    "Origin": "https://apps.dhl.com.hk",
    "Referer": "https://apps.dhl.com.hk/eng_fi/eng_fi_Home.html",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36"
}


def getDataFromDHL(way_num):
    params = {
        "awb": way_num,
        "airbill": way_num
    }
    respnse = requests.post(url=post_url, data=params, headers=hearers)
    print(respnse.text)
    response_html = etree.HTML(respnse.text)
    data = response_html.xpath('//table/tr[2]')
    airwaybill_number = []
    flight_number_vehicle_number = []
    flight_arrival_date = []
    master_airwaybill_number = []
    port_of_loading_country = []
    pieces = []
    print("data ===> %s" % data)
    for i in data:
        airwaybill_number = i.xpath('//td[1]/font/b/text()')
        flight_number_vehicle_number = i.xpath('//td[2]/font/b/text()')
        flight_arrival_date = i.xpath('//td[3]/font/b/text()')
        master_airwaybill_number = i.xpath('//td[4]/font/b/text()')
        port_of_loading_country = i.xpath('//td[5]/font/b/text()')
        pieces = i.xpath('//td[6]/font/b/text()')

    result = {
        "airwaybill_number": airwaybill_number[2],
        "flight_number_vehicle_number": flight_number_vehicle_number[2],
        "flight_arrival_date": flight_arrival_date[2],
        "master_airwaybill_number": master_airwaybill_number[2],
        "port_of_loading_country": port_of_loading_country[2],
        "pieces": pieces[1]
    }
    return result

app = Flask(__name__)

@app.route('/api/get_air_data', methods=['POST'])
def get_person_money_limit():
    try:
        data = request.get_data()
        j_data = json.loads(data)
        airwaybillNumber = j_data["airwaybillNumber"]
        if airwaybillNumber is None:
            return jsonify({"code": 0, "errmsg": "缺少参数"})
        result = getDataFromDHL(airwaybillNumber)
        # result = json.dumps(result)
        print(result)
        return jsonify({"code": 1, "data": result})
    except Exception as e:
        print("系统错误, 原因:", e)
        return jsonify({"code": 0, "errmsg": "内部错误"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8060)






