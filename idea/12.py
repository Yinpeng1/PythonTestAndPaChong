from selenium import webdriver
driver = webdriver.PhantomJS(executable_path=r"C:\Users\pyin\AppData\Local\Programs\Python\Python36-32\Scripts\phantomjs-2.1.1-windows\phantomjs-2.1.1-windows\bin\phantomjs.exe")
driver.get("http://www.baidu.com")
data = driver.title
print(data)