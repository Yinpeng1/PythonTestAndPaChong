import pymysql
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver import TouchActions

url = "https://kyfw.12306.cn/otn/index/init"

chrome_options = Options()
mobileEmulation = {'deviceName': 'iPhone X'}
mobile_emulation = {
    "deviceMetrics": { "width": 360, "height": 640, "pixelRatio": 3.0},
    "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"
}
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument("disable-infobars");
chrome_options.add_argument('lang=zh_CN.UTF-8')
chrome_options.add_experimental_option('mobileEmulation', mobile_emulation)
driver = webdriver.Chrome("C:\chromedriver\chromedriver.exe",  desired_capabilities = chrome_options.to_capabilities())

driver.set_page_load_timeout(30)
driver.get(url)
driver.set_window_size(1920, 1080)
driver.save_screenshot('1.png')

