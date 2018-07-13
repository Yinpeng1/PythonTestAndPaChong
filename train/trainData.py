# !/usr/bin/env python
# -*- coding:utf-8 -*-
import time
import pymysql
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from PIL import ImageFilter
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from aip import AipOcr
from PIL import Image
from aip import AipImageClassify
import re
import requests

APP_ID1 = '11483939'
API_KEY1 = 'M9cQBpPsWCw0SvXIxc0UW7vg'
SECRET_KEY1 = 'GejTozGHBEUP3ku3WGHbjyqGTjgTCncS'

APP_ID2 = '11480013'
API_KEY2 = 'vmarp2WH1hgdpqRoywjHDL78'
SECRET_KEY2 = 'RoTHW97LYFkjPqlQWuouXXxGQEL0QeLk'

client = AipOcr(APP_ID1, API_KEY1, SECRET_KEY1)
client2 = AipImageClassify(APP_ID2, API_KEY2, SECRET_KEY2)

# 准备一下头
headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Cookie": "Hm_lvt_39418dcb8e053c84230016438f4ac86c=1526433568; Hm_lpvt_39418dcb8e053c84230016438f4ac86c=1526433568",
    "Host": "biz.trace.ickd.cn",
    "Referer": "http://103.46.128.47:47720/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"
}

class TrainTicketSpider(object):

    def __init__(self, depCity, arrCity, depdate):
        self.depCity = depCity
        self.arrCity = arrCity
        self.depDate = depdate
        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--disable-gpu')
        # chrome_options.add_argument("--proxy-server=http://39.135.24.11:80")
        self.browser = webdriver.Chrome("C:\chromedriver\chromedriver.exe", chrome_options=chrome_options)

    def crawl(self, url):
        # self.browser.set_page_load_timeout(30)
        self.browser.get(url)
        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.ID, "fromStationText")))
        time.sleep(1)
        self.browser.save_screenshot('1.png')
        # searchType = self.browser.find_element_by_id("fromStationText")
        # 始发地
        fromCity = self.browser.find_element_by_id("fromStationText")

        # 目的地
        toCity = self.browser.find_element_by_id("toStationText")

        # 出发时间
        # jsString = "document.getElementsByName('departDate')[0].removeAttribute('readonly')"
        # self.browser.execute_script(jsString)
        date = self.browser.find_element_by_id("train_date")

        # 搜索按钮
        searchBtn = self.browser.find_element_by_id("query_ticket")

        fromCity.click()
        time.sleep(0.5)
        fromCity.send_keys(self.depCity)
        fromCityClick = self.browser.find_element_by_id("citem_0")
        time.sleep(1)
        fromCityClick.click()

        toCity.click()
        time.sleep(0.5)
        toCity.send_keys(self.arrCity)
        toCityClick = self.browser.find_element_by_id("citem_1")
        time.sleep(1)
        toCityClick.click()

        date.click()
        time.sleep(0.5)
        date.send_keys(self.depDate)

        searchBtn.click()
        WebDriverWait(self.browser, 6).until(EC.presence_of_element_located((By.CLASS_NAME, "t-list")))
        time.sleep(2)
        # self.browser.switch_to.window(self.browser.window_handles[1])
        # self.browser.save_screenshot('3.png')

        try:
            self.parse(current_page=1, date=self.depDate)
        except Exception as e:
            print("爬取失败", e)
            self.browser.quit()

    def parse(self, current_page, date):
        html = self.browser.page_source
        HTML = etree.HTML(html)

        fly_list = HTML.xpath('//tbody[@id="queryLeftTable"]/tr')

        for li in fly_list:
            if li.xpath(".//td"):
                self.getData(li, date)
            else:
                continue

        print('爬取结束')
        # 关闭数据库
        self.browser.quit()

    def get_file_content(self, filePath):
        with open(filePath, 'rb') as fp:
             return fp.read()

    def getData(self, li, date):
        # 车次/类型
        train = li.xpath('.//td[1]/div[1]/div[@class="train"]/div[1]/a/text()')[0]
        # print('正在获取车次型号>>>', train)

        start_station = li.xpath('.//td[1]/div[1]/div[@class="cdz"]/strong[1]/text()')[0]
        end_station = li.xpath('.//td[1]/div[1]/div[@class="cdz"]/strong[2]/text()')[0]

        # 起飞时间/到达时间
        start_time = li.xpath('.//td[1]/div[1]/div[@class="cds"]/strong[@class="start-t"]/text()')[0]
        end_time = li.xpath('.//td[1]/div[1]/div[@class="cds"]/strong[@class="color999"]/text()')[0]

        # 飞行时间
        duration = li.xpath('.//td[1]/div[1]/div[@class="ls"]/strong/text()')[0].strip('\n ')

        # 参考票价
        if li.xpath('.//td[@class="no-br"]/a'):
            ticket_remain = "有"
            ticket_click = self.browser.find_elements_by_xpath('.//td[@class="no-br"]/a')[0]
            ticket_click.click()
            # print(self.browser.window_handles)
        else:
            ticket_remain = "没有"
        print('当前车次%s,[%s]票>>>' % (train, ticket_remain))

    def check_img(self, result, need_text):
        for i in result['result']:
            if need_text in i['keyword'] or i['keyword'] in need_text:
                print("符合要求")
                return 1
            # for j in text:
            #     if j in i['keyword']:
            #          print("符合要求")
            #          return 1


if __name__ == '__main__':
    url = 'https://kyfw.12306.cn/otn/leftTicket/init'
    spider = TrainTicketSpider(depCity="上海", arrCity="北京", depdate="2018-07-20")
    spider.crawl(url)




# if __name__ == '__main__':
#     url = 'https://kyfw.12306.cn/otn/login/init'
#     spider = TrainTicketSpider(depCity="上海", arrCity="北京", depdate="2018-07-20")
#     text = spider.get_img(url)
#     aa = spider.identityUmg()
#     for i in aa:
#         arr = str(i).split(" ")
#         for j in arr:
#             if int(j) > 4:
#                 y = 1
#                 x = int(j) - 1 - 4
#             else:
#                 y = 0
#                 x = int(j) - 1
#             left = 5 + (67 + 5) * x
#             top = 41 + (67 + 5) * y
#             right = left + 67
#             bottom = top + 67
#             action = ActionChains(spider.browser)
#             action.move_to_element_with_offset(spider.browser.find_element_by_class_name("touclick-image"), left + 40, top + 40).click().perform()


