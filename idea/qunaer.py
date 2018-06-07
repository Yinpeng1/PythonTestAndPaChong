import requests
import json
import time
from urllib.parse import quote


s = requests.Session()

depCity = input("请输入始发城市: ")
arrCity = input("请输入到大城市: ")
encodeDepCity = quote(depCity)
encodeArrCity = quote(arrCity)
time = (time.time())*1000
timeJava = str(time).split(".")[0]
# print(encodeDepCity)
# print(encodeArrCity)

# 准备一下头
headers1 = {
    "authority": "flight.qunar.com",
    "method": "GET",
    "path": "/twell/flight/inter/search?depCity="+encodeDepCity+"&arrCity="+encodeArrCity+"&depDate=2018-06-06&adultNum=1&childNum=0&from=qunarindex&ex_track=&es=OuQFutWvOXI2uQW2FtI2csKOFtve2YWuFtEu%3D%3D%3D%3D%7C1528092979768",
    "scheme": "https",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cookie": "QN99=8069; QN1=eIQjmlsU13C0j54oEJp1Ag==; QunarGlobal=192.168.31.65_-7172536f_163c8cd1482_-353d|1528092529191; QN205=auto_4e0d874a; QN277=auto_4e0d874a; csrfToken=QppmKvuKjUlFljGkNfpTnMLY6opUHus4; "
              "QN601=1dd5f0bb4f306e82fecd9e3a2d138b13; _i=VInJO_SDOhfVi2q1ZTglMptutYwq; QN163=0; QN269=BFA372C267BD11E8A85EFA163E9BF76E; "
              "QN6=auto_4e0d874a; QN48=tc_41a79216f16a939a_163c96994f1_976c; cto_lwid=b50e8d2e-40a2-4209-b108-a8c44c73a914; QN243=3; SplitEnv=D; "
              "QN621=1490067914133%3DDEFAULT%26fr%3Dqunarindex; QN170=180.169.230.186_745e7b_0_qH9g7xcJw4uefX7CVfrAo%2FPBHMsinrVHK6XcU%2FZuLxE%3D; "
              "QN300=3W; _vi=oTWCPaKXuKln1bPqjgeEQ_xrI2LGoa5ovbHXOzKvKIX3GjukQ2caAuthkuUuN9wVLddwfxe_TAiEsNLVJUGYzvF-9lJHudozPoT_lO9OiLvHDZogVOtftkkmkWMMn_EyHY4NTzxmRc06IG-ygeWMZRDoij0YNQCRQ90ITaL09Ff8; "
              "Hm_lvt_75154a8409c0f82ecd97d538ff0ab3f3=1528104210,1528108535,1528161784,1528163882;"
              "Hm_lpvt_75154a8409c0f82ecd97d538ff0ab3f3=1528163882;"
              "QN268=|"+timeJava+"_a6f6de772863f789",
    "Referer": "https://flight.qunar.com/site/oneway_list_inter.htm?searchDepartureAirport=%E4%B8%8A%E6%B5%B7&searchArrivalAirport=%E6%9B%BC%E8%B0%B7&searchDepartureTime=2018-06-06&searchArrivalTime=2018-06-27&nextNDays=0&startSearch=true&fromCode=SHA&toCode=BKK&from=qunarindex&lowestPrice=null&favoriteKey=&showTotalPr=null&adultNum=1&childNum=0&cabinClass=",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"
}


# 准备一下头
headers = {
    "authority": "flight.qunar.com",
    "method": "GET",
    "path": "/twell/flight/inter/search?depCity="+encodeDepCity+"&arrCity="+encodeArrCity+"&depDate=2018-06-06&adultNum=1&childNum=0&from=qunarindex&ex_track=&es=OuQFutWvOXI2uQW2FtI2csKOFtve2YWuFtEu%3D%3D%3D%3D%7C1528092979768",
    "scheme": "https",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cookie": "QN99=8069; QN1=eIQjmlsU13C0j54oEJp1Ag==; QunarGlobal=192.168.31.65_-7172536f_163c8cd1482_-353d|1528092529191; QN205=auto_4e0d874a; QN277=auto_4e0d874a; csrfToken=QppmKvuKjUlFljGkNfpTnMLY6opUHus4; "
              "QN601=1dd5f0bb4f306e82fecd9e3a2d138b13; _i=VInJO_SDOhfVi2q1ZTglMptutYwq; QN163=0; QN269=BFA372C267BD11E8A85EFA163E9BF76E; "
              "QN6=auto_4e0d874a; QN48=tc_41a79216f16a939a_163c96994f1_976c; cto_lwid=b50e8d2e-40a2-4209-b108-a8c44c73a914; QN243=3; SplitEnv=D; "
              "QN621=1490067914133%3DDEFAULT%26fr%3Dqunarindex; QN170=180.169.230.186_745e7b_0_qH9g7xcJw4uefX7CVfrAo%2FPBHMsinrVHK6XcU%2FZuLxE%3D; "
              "QN300=3W; _vi=oTWCPaKXuKln1bPqjgeEQ_xrI2LGoa5ovbHXOzKvKIX3GjukQ2caAuthkuUuN9wVLddwfxe_TAiEsNLVJUGYzvF-9lJHudozPoT_lO9OiLvHDZogVOtftkkmkWMMn_EyHY4NTzxmRc06IG-ygeWMZRDoij0YNQCRQ90ITaL09Ff8; "
              "Hm_lvt_75154a8409c0f82ecd97d538ff0ab3f3=1528104210,1528108535,1528161784,1528163882;"
              "Hm_lpvt_75154a8409c0f82ecd97d538ff0ab3f3=1528163882;"
              "QN268=|"+timeJava+"_a6f6de772863f789",
    "Referer": "https://flight.qunar.com/site/oneway_list_inter.htm?searchDepartureAirport=%E4%B8%8A%E6%B5%B7&searchArrivalAirport=%E6%9B%BC%E8%B0%B7&searchDepartureTime=2018-06-06&searchArrivalTime=2018-06-27&nextNDays=0&startSearch=true&fromCode=SHA&toCode=BKK&from=qunarindex&lowestPrice=null&favoriteKey=&showTotalPr=null&adultNum=1&childNum=0&cabinClass=",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"
}

values1 = {
   "depCity": depCity,
   "arrCity": arrCity,
   "depDate": "2018-06-06",
   "adultNum": "1",
   "childNum": "0",
   "from": "qunarindex",
   "ex_track": "",
   "es": "4nt+gZyCJT9JIZDCMcjagyqCMZobjEtCMZjJ====|"+timeJava
}
values2 = {
    "depCity": depCity,
    "_": 1528164524554
}

values = {
   "depCity": depCity,
   "arrCity": arrCity,
   "depDate": "2018-06-06",
   "adultNum": "1",
   "childNum": "0",
   "from": "qunarindex",
   "ex_track": "",
   "queryId": "10.90.57.100:l:2434c38e:163cd9af330:-7a1c",
   "es": "4ntqIHVCaTjjgtVCMZjug4E84TjJgyDCHTb8IE9NCCy+IE9C|"+timeJava
}
url1 = 'https://flight.qunar.com/twell/flight/inter/search?depCity='+encodeDepCity+'&arrCity='+encodeArrCity+'&depDate=2018-06-06&adultNum=1&childNum=0&from=qunarindex&ex_track=&es=4nt%2BgZyCJT9JIZDCMcjagyqCMZobjEtCMZjJ%3D%3D%3D%3D%7C'+timeJava
# request1 = s.get(url=url1, params=values1, headers=headers1)
# url2 = 'https://flight.qunar.com/twell/flight/inter/localdate?depCity=%E4%B8%8A%E6%B5%B7&_=1528164524554'
# request2 = s.get(url=url2, params=values2, headers=headers1)
url1 = 'https://flight.qunar.com/twell/flight/inter/search?depCity='+encodeDepCity+'&arrCity='+encodeArrCity+'&depDate=2018-06-06&adultNum=1&childNum=0&from=qunarindex&ex_track=&es=4nt%2BgZyCJT9JIZDCMcjagyqCMZobjEtCMZjJ%3D%3D%3D%3D%7C'+timeJava
request1 = s.get(url=url1, params=values, headers=headers)
# url = 'https://flight.qunar.com/twell/flight/inter/search?depCity=%E4%B8%8A%E6%B5%B7&arrCity=%E6%9B%BC%E8%B0%B7&depDate=2018-06-06&adultNum=1&childNum=0&ex_track=&from=qunarindex&queryId=10.90.57.100%3Al%3A2434c38e%3A163cd9af330%3A-76cf&es=4ntagyyCtHj%2BgtV8MZjug4E84TjJgtyC4HjJg4VC4ny%2BugIjZny%2Bg%3D%3D%3D%7C'+timeJava
# request = s.get(url=url, params=values, headers=headers)

# 自动解码
# s = json.loads(request1.text)
print(s)
print(s["result"]["ctrlInfo"])
print("ctrlInfo info end=====================")
print(s["result"]["filters"])
print("filters info end=====================")
print(s["result"]["flightPrices"])
print("flightPrices info end=====================")
print(s["result"]["most"])
print("flightPrices info end=====================")

result = s["result"]["flightPrices"]


# s = quote("上海")
# print(s)
for i in result:
    print(i)
    # print(i["journey"])
    # print(i["price"]["lowTotalPrice"])






# print(time.time())
# 1528100936
# 1528101023825_a6f6de772863f789
#
# 1528099898;
# QN268=|1528099983518_65ab1b81b2d1aa51
#
# 1528100936;
# QN268=|1528101023825_a6f6de772863f789