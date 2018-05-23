#!C:\Users\pyin\AppData\Local\Programs\Python\Python36-32\python.exe

import cgi, cgitb

form = cgi.FieldStorage()

site_name = form.getvalue('name')
site_url = form.getvalue('url')

print("Content-type:text/html")
print()
print("<html>")
print("<head>")
print("<meta http-equiv=”Content-Type” content=”text/html; charset=UTF-8”/>")
print("<title>菜鸟教程 CGI 测试实例</title>")
print("</head>")
print("<body>")
print("<h2>%s官网：%s</h2>" % (site_name, site_url))
print("</body>")
print("</html>")
