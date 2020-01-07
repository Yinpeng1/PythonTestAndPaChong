import requests

# headers = {
#     "Accept": "*/*",
#     "Accept-Encoding": "gzip, deflate, br",
#     "Accept-Language": "zh-CN,zh;q=0.9",
#     "Connection": "keep-alive",
#     "Cookie": "s_ViewType=10; _lxsdk_cuid=16b64057331c8-05c69c9af97c34-591d3314-1fa400-16b64057331c8; _lxsdk=16b64057331c8-05c69c9af97c34-591d3314-1fa400-16b64057331c8; _hc.v=341c7afe-50b5-c870-3374-ef74f8e86e49.1560751208; cy=1; cye=shanghai; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_s=16bc1a0e2b0-c35-403-0ee%7C%7C146",
#     "Host": "www.dianping.com",
#     "Referer": "https://www.dianping.com/search/keyword/1/0_GUCCI",
#     "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
#     "X-Requested-With": "XMLHttpRequest"
# }
# response = requests.get("https://www.dianping.com/search/keyword/1/0_GUCCI", headers=headers)
# print(response.text)

s = "https://www.dianping.com/search/keyword/1/0_Gucci/p2"
print(s.replace("https://www.dianping.com/search/keyword/1/0_", ""))

# current_url = response.request.url
currrent_band = str(s).replace("https://www.dianping.com/search/keyword/1/0_", "")
if "/p" in currrent_band:
    num = currrent_band.index("/")
    currrent_band = currrent_band[0: num]
print(currrent_band)
