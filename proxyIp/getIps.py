# !/usr/bin/env python
# -*- coding:utf-8 -*-
import time
import pymysql
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import sys
import os

class TrainTicketSpider(object):

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        # chrome_options.add_argument("--proxy-server=http://39.135.24.11:80")
        self.browser = webdriver.Chrome("C:\chromedriver\chromedriver.exe", chrome_options=chrome_options)
        # print(self.browser.get("http://httpbin.org/ip"))
        self.connection = pymysql.connect(host='47.98.102.190',
                                          user='root',
                                          password='123',
                                          db='test',
                                          port=3306,
                                          charset='utf8',  # 不能用utf-8
                                          cursorclass=pymysql.cursors.DictCursor)

    def crawl(self, url):
        # self.browser.set_page_load_timeout(30)
        self.browser.get(url)
        self.browser.save_screenshot('1.png')

        WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "service-head")))
        time.sleep(2)
        self.browser.save_screenshot('3.png')

        try:
            self.parse()
        except Exception as e:
            print("爬取失败", e)
            if self.connection:
                self.connection.close()
            self.browser.quit()

    def parse(self):
        html = self.browser.page_source
        HTML = etree.HTML(html)

        fly_list = HTML.xpath('//div[@class="wlist"]/ul/li[2]/ul')

        for li in fly_list:
            if li.xpath("./span[1]/li/text()")[0] == "IP":
                continue
            else:
                self.getData(li)

        print('爬取结束')
        # 关闭数据库
        self.connection.close()
        self.browser.quit()

    def getData(self, li):
        # 航空公司/类型
        ip = li.xpath('.//span[1]/li/text()')[0]
        port = li.xpath('.//span[2]/li/text()')[0]
        type = li.xpath('.//span[4]/li/a/text()')[0]
        country = li.xpath('.//span[5]/li/a/text()')[0]

        print("正在获取ip：" + ip + ":" + port)
        # 保存到MySQL数据库
        self.save(ip, port, type, country)

    def save(self, ip, port, type, country):
        with self.connection.cursor() as cursor:
            sql = 'INSERT INTO proxy_ip(ip, port, type, country) VALUES (%s,%s,%s,%s)'
            sql2 = "select * from proxy_ip where ip = '%s' and port = '%s'"
            cursor.execute(sql2)

            lists = cursor.fetchall()
            if lists:
                pass
            else:
                cursor.execute(sql, (ip, port, type, country))
        self.connection.commit()



if __name__ == '__main__':

    while 1 > 0:
        url = 'http://www.data5u.com/'
        spider = TrainTicketSpider()
        # spider = TrainTicketSpider(depCity=sys.argv[1], arrCity=sys.argv[2], depdate=sys.argv[3])
        spider.crawl(url)
        time.sleep(300)
