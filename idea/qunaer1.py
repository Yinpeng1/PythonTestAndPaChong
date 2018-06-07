import requests
import json
import time
from urllib.parse import quote


# depCity = input("请输入始发城市: ")
# arrCity = input("请输入到大城市: ")
# encodeDepCity = quote(depCity)
# encodeArrCity = quote(arrCity)
time = (time.time())*1000
timeJava = str(time).split(".")[0]

header = {
        # "authority": "flight.qunar.com",
        # "method": "GET",
        # "path": "/twell/flight/inter/search?depCity=%E4%B8%8A%E6%B5%B7&arrCity=%E6%9B%BC%E8%B0%B7&depDate=2018-09-07&adultNum=1&childNum=0&from=flight_int_search&ex_track=&es=56ullFrsOFrC2%2FfsXXFpCOrWXXK5KWfPXX6q%3D%3D%3D%3D%7C1528350744443",
        # "scheme": "https",
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cookie": 'QN99=8069; QN1=eIQjmlsU13C0j54oEJp1Ag==; QunarGlobal=192.168.31.65_-7172536f_163c8cd1482_-353d|1528092529191; '
                  'csrfToken=QppmKvuKjUlFljGkNfpTnMLY6opUHus4; QN601=1dd5f0bb4f306e82fecd9e3a2d138b13; _i=VInJO_SDOhfVi2q1ZTglMptutYwq; '
                  'QN163=0; QN269=BFA372C267BD11E8A85EFA163E9BF76E; QN48=tc_41a79216f16a939a_163c96994f1_976c; '
                  'cto_lwid=b50e8d2e-40a2-4209-b108-a8c44c73a914; SplitEnv=D; '
                  'QN170=180.169.230.186_745e7b_0_qH9g7xcJw4uefX7CVfrAo%2FPBHMsinrVHK6XcU%2FZuLxE%3D; QN300=auto_4e0d874a; QN70=1502bdb5a163cde697f0; '
                  '__utma=183398822.559978338.1528167746.1528167746.1528167746.1; __utmc=183398822; '
                  '__utmz=183398822.1528167746.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); '
                  '_jzqa=1.1815039428106608400.1528167747.1528167747.1528167747.1; '
                  '_jzqc=1; _jzqx=1.1528167747.1528167747.1.jzqsr=hotel%2Equnar%2Ecom|jzqct=/.-; hjstat_uv=851237833423693777|682523; '
                  'QN171="duomai,52063819,228451"; _vi=pf6jeKrLE4iXr-yEwERmdHmS-FGeAgPH_UmhiHASS9pxowNGLSLw3l9MmqiWP7suS6NuD-kLlDixQkLunjUmLa6rYEoaSZaatji8Jlvhwz0pSxJGVAnXfg6L_3IeuqYoVX0_dyoXJkGQuBjQpRi9xxCjLBiO8rAFQsGuxOYdFlVd; '
                  'activityClose=1; QN621=1490067914133%3DDEFAULT%26fr%3Dflight_int_search; '
                  'Hm_lvt_75154a8409c0f82ecd97d538ff0ab3f3=1528164513,1528167773,1528353266,1528353398; '
                  'Hm_lpvt_75154a8409c0f82ecd97d538ff0ab3f3=1528353398; QN268=|1528353486012_3047f0b2f53394c4; '
                  'hjstat_ss=502038510_1_1528382199_682523; QN205=auto_52b3f121; QN277=auto_52b3f121; QN6=auto_52b3f121; QN243=17; '
                  'RT=s=1528353611966&r=https%3A%2F%2Fflight.qunar.com%2F',
        "referer": "https://flight.qunar.com/site/oneway_list_inter.htm?searchDepartureAirport=%E4%B8%8A%E6%B5%B7&searchArrivalAirport=%E6%9B%BC%E8%B0%B7&searchDepartureTime=2018-09-07&searchArrivalTime=2018-09-14&nextNDays=0&startSearch=true&fromCode=SHA&toCode=BKK&from=flight_int_search&lowestPrice=null&favoriteKey=&showTotalPr=0&adultNum=1&childNum=0&cabinClass=",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"
}

values = {
    "depCity": "上海",
    "arrCity": "曼谷",
    "depDate": "2018-09-07",
    "adultNum": 1,
    "childNum": 0,
    "from": "flight_int_search",
    "ex_track": "",
    "es": "56upCbfPlFyj2OfsXXFpCOrWXXK5KWfPXX6q====|1528350744443"
}

url = "https://flight.qunar.com/twell/flight/inter/search?depCity=%E4%B8%8A%E6%B5%B7&arrCity=%E6%9B%BC%E8%B0%B7&depDate=2018-09-07&adultNum=1&childNum=0&from=flight_int_search&ex_track=&es=56upCbfPlFyj2OfsXXFpCOrWXXK5KWfPXX6q%3D%3D%3D%3D%7C1528350744443"

response = requests.get(url=url, params=values, headers=header)
s = json.loads(response.text)
print(s["result"]["flightPrices"])
print(len(s))
