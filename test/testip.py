import requests

# proxy = {
#     # 'http': 'http://117.85.105.170:808',
#     # 'https': 'https://117.85.105.170:808'
#     # 'http': 'http://165.227.62.167:8080'
#     'http': "117.191.11.102:8080"
# }
# '''head 信息'''
# head = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
#              'Connection': 'keep-alive'}
# p = requests.get('http://icanhazip.com', headers=head, proxies=proxy)
# print(p.text)


from urllib.parse import unquote
print(unquote("sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22167832cb7737c5-088b25a9aa7982-5d1e331c-2073600-167832cb7748ed%22%2C%22%24device_id%22%3A%22167832cb7737c5-088b25a9aa7982-5d1e331c-2073600-167832cb7748ed%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Flink%22%2C%22%24latest_referrer_host%22%3A%22www.baidu.com%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%7D%2C%22first_id%22%3A%22%22%7D"))

