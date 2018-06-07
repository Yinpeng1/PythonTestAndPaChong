import requests
import re

url = 'https://flight.qunar.com/'
request23 = requests.get(url=url)
t = request23.text
print(t)

route = re.compile(r'<ul class="ul_route_lst">(.*)</ul>')  # 正则匹配，compile为把正则表达式编译成一个正则表达式对象，提供效率。
routeRe = re.findall(route, t)  # 获取字符串中所有匹配的字符串
print(routeRe)

for i in routeRe:
    li = re.compile(r'<li>(.*)</li>')  # 正则匹配，compile为把正则表达式编译成一个正则表达式对象，提供效率。
    liRe = re.findall(li, i)  # 获取字符串中所有匹配的字符串
    print(liRe)
