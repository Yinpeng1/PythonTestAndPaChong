import requests
import time

s = requests.session()



headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded",
    "Cookie": "SINAGLOBAL=8811239590552.908.1554795512076; _s_tentry=bbs.51testing.com; UOR=www.mobiletrain.org,widget.weibo.com,bbs.51testing.com; "
              "YF-V5-G0=2583080cfb7221db1341f7a137b6762e; SUB=_2AkMrqVZwf8NxqwJRmP4Rzmrnb41www3EieKd9aerJRMxHRl-yT83qmELtRB6ACl4nofRmxDzqfMwsA1CDIhMiHkglQxF; "
              "SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WWAqzj9_10uF1TnFsaIFn4M; Apache=2812842655699.9966.1559615819325; "
              "ULV=1559615819334:2:1:1:2812842655699.9966.1559615819325:1554795512085; "
              "YF-Page-G0=bd9e74eeae022c6566619f45b931d426|1559616130|1559616130",
    "Host": "weibo.com",
    "Referer": "https://weibo.com/u/5326891113?profile_ftype=1&is_all=1",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}

currentTime = str(time.time() * 1000).split('.')[0]

url = "https://weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain=100505&profile_ftype=1&is_all=1" \
      "&pagebar=1&pl_name=Pl_Official_MyProfileFeed__20&id=1005055326891113&script_uri=/u/5326891113&feed_type=0&page=1&pre_page=1&domain_op=100505" \
      "&__rnd=" + currentTime

"https://weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain=100505&is_search=0&visible=0&is_all=1&is_tag=0&profile_ftype=1" \
"&page=5&pagebar=0&pl_name=Pl_Official_MyProfileFeed__20&id=1005055326891113" \
"&script_uri=/u/5326891113&feed_type=0&pre_page=5&domain_op=100505&__rnd=1559618337435"

response = s.get(url=url, headers=headers)
print(response.encoding)
print(response.text.encode('utf-8').decode('unicode_escape'))
print("\u63a8\u5e7f")

href="/u/5326891113?pids=Pl_Official_MyProfileFeed__20&is_search=0&visible=0&is_all=1&is_tag=0&profile_ftype=1&page=3#feedtop"

