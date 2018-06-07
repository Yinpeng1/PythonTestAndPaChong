import requests
import time
import json
from urllib.parse import unquote

time = (time.time())*1000
timeJava = str(time).split(".")[0]
headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Content-Type": "application/json",
    "Connection": "keep-alive",
    "Content-Length": "434",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": "JSESSIONID=C5A683EDA5FA48FDD64627026DA08515; language=zh_CN; zsluserCookie=true; sid=c9d43280ff124596b97b5efcac2db06e; "
              "temp_zh=cou%3D0%3Bsegt%3D%E5%8D%95%E7%A8%8B%3Btime%3D2018-06-06%3B%E5%8C%97%E4%BA%AC-%E5%93%88%E5%B0%94%E6%BB%A8%3B1%2C0%2C0%3B%26; "
              "JSESSIONID=C95B1E1EE5D9659D8E4110EA41E76123; WT-FPC=id=180.169.230.186-1059380208.30669952:lv="+timeJava+":ss=1528177159222:fs=1528170512003:pn=3:vn=1; "
              "WT.al_flight=WT.al_hctype(S)%3AWT.al_adultnum(1)%3AWT.al_childnum(0)%3AWT.al_infantnum(0)%3AWT.al_orgcity1(PEK)%3AWT.al_dstcity1(HRB)%3AWT.al_orgdate1(2018-06-06)",
    "Host": "b2c.csair.com",
    "Origin": "https://b2c.csair.com",
    "Referer": "https://b2c.csair.com/B2C40/modules/bookingnew/main/flightSelectDirect.html?t=S&c1=PEK&c2=HRB&d1=2018-06-06&at=1&ct=0&it=0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}

values = {
    "depcity": "PEK",
    "arrcity": "HRB",
    "flightDate": "20180606",
    "adultnum": "1",
    "childnum": "0",
    "infantnum": "0",
    "cabinorder": "0",
    "airline": "1",
    "flytype": "3",
    "international": "0",
    "action": "0",
    "segtype": "1",
    "cache": "0",
    "isMember": "",
    "preUrl": "",
    "cabinOrder": "0"

}

url = "https://b2c.csair.com/portal/flight/direct/query"

print(unquote("cou%3D0%3Bsegt%3D%E5%8D%95%E7%A8%8B%3Btime%3D2018-06-06%3B%E5%8C%97%E4%BA%AC-%E5%93%88%E5%B0%94%E6%BB%A8%3B1%2C0%2C0%3B%26"))

# response = requests.post(url=url, params=json.dumps(values), headers=headers)
#
# print(response.text)

