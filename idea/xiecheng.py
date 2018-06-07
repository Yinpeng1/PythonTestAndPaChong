import requests
from urllib.parse import quote
from urllib.parse import unquote
import json
import urllib
import time
import sys

s = requests.session();

depCity = input("请输入始发城市: ")
arrCity = input("请输入到大城市: ")
encodeDepCity = quote(depCity)
encodeArrCity = quote(arrCity)
encodeGBKDepCity = quote(depCity, encoding="gb2312")
encodeGBKArrCity = quote(arrCity, encoding="gb2312")

time = (time.time())*1000
timeJava = str(time).split(".")[0]

headers1 = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    # "Content-Length": "80"
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": "_RGUID=d9b89c93-0242-4a5d-aa94-17874e57f587",
    "Host": "cdid.c-ctrip.com",
    "Origin": "http://trains.ctrip.com",
    "Referer": "http://trains.ctrip.com/TrainBooking/Search.aspx?from=shanghai&to=changsha&day=52&number=&fromCn="+encodeDepCity+"&toCn="+encodeArrCity,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"
}

headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    # "Cache-Control": "max-age=0",
    # "Connection": "keep-alive",
    # "Content-Length": "319",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": '_abtest_userid=bc7d5a9d-e30a-4061-9949-1a18f5b595a3; '
              '_ga=GA1.2.1006336392.1528103104; '
              'traceExt=campaign=CHNbaidu81&adid=index; '
              'MKT_Pagesource=PC; '
              'manualclose=1; _RF1=180.169.230.186; _RSG=TfaG2C9ducD7M_LETu5KgA; '
              '_RDG=28b6f82946f68720783ae8f73057b03ba0; _RGUID=d9b89c93-0242-4a5d-aa94-17874e57f587; '
              'FlightIntl=Search=[%22SHA|%E4%B8%8A%E6%B5%B7(SHA)|2|SHA|480%22%2C%22LAX|%E6%B4%9B%E6%9D%89%E7%9F%B6(LAX)|347|LAX|480%22%2C%222018-06-06%22]; '
              'Session=SmartLinkCode=U155935&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=&SmartLinkLanguage=zh; '
              'adscityen=Shanghai; _gid=GA1.2.1727226027.1528191733; '
              'FD_SearchHistorty={"type":"S","data":"S%24%u4E0A%u6D77%28SHA%29%24SHA%242018-06-08%24%u5317%u4EAC%28BJS%29%24BJS"}; '
              'ASP.NET_SessionSvc=MTAuMTQuMS4xNzZ8OTA5MHxvdXlhbmd8ZGVmYXVsdHwxNTI1Njc2NTgwMDMy; Union=SID=155952&AllianceID=4897&OUID=baidu81|index|||;'
              ' Mkt_UnionRecord=%5B%7B%22aid%22%3A%224897%22%2C%22timestamp'+quote(timeJava)+'%7D%5D; '
              '__zpspc=9.5.1528192048.1528192479.6%231%7Cbaiduppc%7Cbaidu%7Cty%7C%25E6%259C%25BA%25E7%25A5%25A8%7C%23; '
              '_jzqco=%7C%7C%7C%7C1528191737931%7C1.1163070240.1528103108870.1528192465330.1528192479371.1528192465330.1528192479371.undefined.0.0.15.15; '
              '_bfi=p1%3D108001%26p2%3D108001%26v1%3D20%26v2%3D17; '
              '_bfa=1.1528103097722.2eduvl.1.1528103097722.1528191730649.4.32; _bfs=1.2',
    "Host": "trains.ctrip.com",
    "If-Modified-Since": "Thu, 01 Jan 1970 00:00:00 GMT",
    "Origin": "http://trains.ctrip.com",
    "Referer": "http://trains.ctrip.com/TrainBooking/Search.aspx?from=shanghai&to=changsha&day=52&number=&fromCn="+encodeGBKDepCity+"3&toCn="+encodeGBKArrCity,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"
}

values1 = {
    "requestId": "d9b89c9302424a5daa9417874e57f587_17",
    "serverName": "http://trains.ctrip.com"
}

value = {
    "IsBus": "false",
    "Filter": "3",
    "Catalog": "",
    "IsGaoTie": "false",
    "IsDongChe": "false",
    "CatalogName": "",
    "DepartureCity": "shanghai",
    "ArrivalCity": "changsha",
    "HubCity": "",
    "DepartureCityName": "上海",
    "ArrivalCityName": "长沙",
    "DepartureDate": "2018-06-06",
    "DepartureDateReturn": "2018-06-08",
    "ArrivalDate": "",
    "TrainNumber": ""
}
url = "http://cdid.c-ctrip.com/model-poc2/h"
url2 = "http://trains.ctrip.com/TrainBooking/Ajax/SearchListHandler.ashx?Action=getSearchList"


# 创建一个request,放入我们的地址、数据、头
# request23 = urllib.request.Request(url, headers=headers1)

# data = urllib.parse.urlencode(values1).encode('utf-8')
response = s.post(url=url, params=values1, headers=headers1)
print(response.text)
# print(value)
# print(json.dumps(value))
response2 = s.post(url=url2, params=value, headers=headers)
# page = urllib.request.urlopen(request23, data).read().decode('latin-1')
print(response2.text)


# print(("%C9%CF%BA%A3").decode("utf-8"))
# print(quote("上海", encoding='gb2312'))
# print(unquote("%E6%9C%BA%E7%A5%A8"))
# print(unquote("9.5.1528192048.1528192479.6%231%7Cbaiduppc%7Cbaidu%7Cty%7C%25E6%259C%25BA%25E7%25A5%25A8%7C%23;"))
# print(unquote("%7C%7C%7C%7C1528191737931%7C1.1163070240"))
# print(unquote("[%22SHA|%E4%B8%8A%E6%B5%B7(SHA)|2|SHA|480%22%2C%22LAX|%E6%B4%9B%E6%9D%89%E7%9F%B6(LAX)|347|LAX|480%22%2C%222018-06-06%22]"))
# print(unquote("%22%3A1528252792907%7D%5D"))


