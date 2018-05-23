#!C:\Users\pyin\AppData\Local\Programs\Python\Python36-32\python.exe
import  cgi, cgitb

form = cgi.FieldStorage()

if form.getvalue("google"):
    google_flag = "是"
else:
    google_flag = "否"

if form.getvalue("runoob"):
    runoob_flag = "是"
else:
    runoob_flag = "否"


print("Content-type:text/html")
print()
print("<html>")
print("<head>")
print("<meta http-equiv=”Content-Type” content=”text/html; charset=UTF-8”/>")
print("<title>菜鸟教程 CGI 测试实例</title>")
print("</head>")
print("<body>")
print("<h2> 菜鸟教程是否选择了 : %s</h2>" % runoob_flag)
print("<h2> Google 是否选择了 : %s</h2>" % google_flag)
print("</body>")
print("</html>")