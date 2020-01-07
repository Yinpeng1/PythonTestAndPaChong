import requests
import json
from flask import Flask, render_template, jsonify, request

url = 'http://47.98.102.190:5000/api/get_person_money_limit'

app = Flask(__name__)

headers = {'Content-Type': 'application/json'}

@app.route('/api/get_person_money_limit', methods=['POST'])
def get_person_money_limit():
    try:
        data = request.get_data()
        j_data = json.loads(data)
        persona_name = j_data["persona_name"]
        id_number = j_data["id_number"]
        if persona_name is None:
            return jsonify({"code": 0, "errmsg": "缺少参数"})
        if id_number is None:
            return jsonify({"code": 0, "errmsg": "缺少参数"})
        data = {
            "persona_name": persona_name,
            "id_number": id_number,
            "user": "im"
        }
        response = requests.post(url=url, data=json.dumps(data), headers=headers)
        result = response.text
        # print(result)
        result = json.loads(result)
        if result["code"] == 0:
            return jsonify({"code": 0, "errmsg": result["errmsg"]})
        else:
            already_use = result["data"]["already_use"]
            money = result["data"]["money"]
            return jsonify({"code": 1, "data": {'already_use': already_use, 'left_use': money}})
    except Exception as e:
        print("系统错误, 原因:", e)
        return jsonify({"code": 0, "errmsg": "内部错误"})

if __name__ == '__main__':
    app.run(host='0.0.0.0')
