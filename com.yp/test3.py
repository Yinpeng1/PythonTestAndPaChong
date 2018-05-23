#!C:\Users\pyin\AppData\Local\Programs\Python\Python36-32\python.exe
print("Content-type:text/html")
print()                             # 空行，告诉服务器结束头部
print('<html>')
print('<head>')
print('<meta http-equiv=”Content-Type” content=”text/html; charset=UTF-8” /> ')
print('<title>Hello Word - 我的第一个 CGI 程序！</title>')
print('</head>')
print('<body>')
print('<h2>Hello Word! 我是来自菜鸟教程的第一CGI程序</h2>')
print('</body>')
print('</html>')

import  os


print("Content-type: text/html")
print()
print("<meta charset=\"utf-8\">")
print("<b>环境变量</b><br>")
print("<ul>")
for key in os.environ.keys():
    print("<li><span style='color:green'>%30s </span> : %s </li>" % (key, os.environ[key]))
print("</ul>")

