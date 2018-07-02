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
    """
    使用Selenium库和PhantomJS浏览器,爬取去哪儿网机票信息
    只实现当日单程票查询
    """

    def __init__(self, depCity, arrCity, depdate):
        self.depCity = depCity
        self.arrCity = arrCity
        self.depDate = depdate
        # dcap = dict(DesiredCapabilities.PHANTOMJS)
        # dcap["phantomjs.page.settings.userAgent"] = (
        #     "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36")
        # dcap["phantomjs.page.settings.loadImages"] = False
        # self.browser = webdriver.PhantomJS(
        #     executable_path=r"C:\Users\pyin\AppData\Local\Programs\Python\Python36-32\Scripts\phantomjs-2.1.1-windows\phantomjs-2.1.1-windows\bin\phantomjs.exe",
        #     desired_capabilities=dcap)
        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--disable-gpu')
        # chrome_options.add_argument("--proxy-server=http://39.135.24.11:80")
        chrome_options.add_argument("--proxy-server=http://219.141.153.12:8080")
        # desired_capabilities = webdriver.DesiredCapabilities.INTERNETEXPLORER.copy()
        # desired_capabilities['proxy'] = {
        #     "httpProxy": "http://114.115.144.137:3128/",
        #     "ftpProxy": "http://114.115.144.137:3128/",
        #     "sslProxy": "http://114.115.144.137:3128/",
        #     "noProxy": None,
        #     "proxyType": "MANUAL",
        #     "class": "org.openqa.selenium.Proxy",
        #     "autodetect": False
        # }
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
        self.browser.set_page_load_timeout(30)
        self.browser.get(url)
        self.browser.set_window_size(1920, 1080)
        self.browser.save_screenshot('1.png')

        searchType = self.browser.find_element_by_class_name("eye-radio-icon")

        # 始发地
        fromCity = self.browser.find_element_by_name("departCityName")

        # 目的地
        toCity = self.browser.find_element_by_name("destCityName")

        # 出发时间
        jsString = "document.getElementsByName('departDate')[0].removeAttribute('readonly')"
        self.browser.execute_script(jsString)
        date = self.browser.find_element_by_name("departDate")

        # 搜索按钮
        searchBtn = self.browser.find_element_by_id("searchIntl")

        aaa = self.browser.find_element_by_class_name("title")

        searchType.click()
        time.sleep(1)

        fromCity.click()
        time.sleep(1)
        fromCity.clear()
        time.sleep(2)
        fromCity.send_keys(self.depCity)
        time.sleep(2)
        aaa.click()
        time.sleep(1)
        # aaa.click(1)
        # time.sleep(1)

        toCity.click()
        time.sleep(1)
        toCity.clear()
        time.sleep(1)
        toCity.send_keys(self.arrCity)
        time.sleep(1)
        aaa.click()
        time.sleep(1)

        date.clear()
        time.sleep(1)
        # date.click()
        date.send_keys(self.depDate)
        time.sleep(2)
        # aaa.click()
        # time.sleep(1)

        # aaa.click()
        searchBtn.click()
        time.sleep(3)
        while self.browser.current_url == 'http://flight.tuniu.com/intel':
            if fromCity.text:
                pass
            else:
                fromCity.clear()
                time.sleep(1)
                self.browser.find_element_by_name("departCityName").send_keys(self.depCity)
                time.sleep(2)
                aaa.click()
                time.sleep(2)

            if toCity.text:
                pass
            else:
                toCity.click()
                time.sleep(1)
                toCity.clear()
                time.sleep(1)
                toCity.send_keys(self.arrCity)
                time.sleep(1)
                aaa.click()
                # toCity.click()
                time.sleep(1)

            searchBtn.click()
            time.sleep(3)
        # self.browser.implicitly_wait(15)
        # time.sleep(16)

        WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "tn-search-list")))
        time.sleep(10)
        # self.browser.switch_to.window(self.browser.window_handles[1])
        self.browser.save_screenshot('3.png')

        try:
            self.parse(current_page=1, date=self.depDate)
        except Exception as e:
            print("爬取失败", e)
            if self.connection:
                self.connection.close()
            self.browser.quit()

    def parse(self, current_page, date):
        html = self.browser.page_source
        HTML = etree.HTML(html)

        fly_list = HTML.xpath('//div[@class="tn-search-list"]/div')

        for li in fly_list:
            self.getData(li, date)

        print('爬取结束')
        # 关闭数据库
        self.connection.close()
        self.browser.quit()

    def getData(self, li, date):
        # 航空公司/类型
        air_company = li.xpath('.//div[@class="flight-row"]/div[@class="flight-item-iataInfo"]/div[@class="airline-name"]/text()')[0]
        air_type = li.xpath('.//div[@class="flight-row"]/div[@class="flight-item-iataInfo"]/div[@class="airline-no"]/text()')[0]
        # air_type = air_type_arr[0] + air_type_arr[1]
        fly_info = air_company + air_type
        print('正在获取飞机型号>>>', fly_info)

        # 起飞机场/到达机场/图转机场
        start_station = li.xpath('.//div[@class="flight-row"]/div[@class="flight-item-schedule"]/div[@class="flight-schedule-s"]/div[@class="flight-schedule-s-airport"]/text()')[0]


        end_station = li.xpath('.//div[@class="flight-row"]/div[@class="flight-item-schedule"]/div[@class="flight-schedule-e"]/div[@class="flight-schedule-e-airport"]/text()')[0]



        transit_airport_title = ""
        transit_airport_city = ""
        transit_airport = ""
        transit_airport_time = ""
        transit_airport_duration = ""
        if li.xpath('.//div[@class="flight-row"]/div[@class="flight-item-more"]/div[@class="flight-stop-info"]/div[@class="stop-city"]/text()'):
            transit_airport_city = li.xpath('.//div[@class="flight-row"]/div[@class="flight-item-more"]/div[@class="flight-stop-info"]/div[@class="stop-city"]/text()')[0]


        STATION = (start_station + '-' + end_station).strip('\n ')

        # 起飞时间/到达时间
        start_time = li.xpath('.//div[@class="flight-row"]/div[@class="flight-item-schedule"]/div[@class="flight-schedule-s"]/div[@class="flight-schedule-s-time"]/text()')[0]
        end_time = li.xpath('.//div[@class="flight-row"]/div[@class="flight-item-schedule"]/div[@class="flight-schedule-e"]/div[@class="flight-schedule-e-time"]/text()')[0]

        # 飞行时间
        duration = li.xpath('.//div[@class="flight-row"]/div[@class="flight-item-more"]/div[@class="flight-total-time"]/text()')[0].strip('\n ')

        # 参考票价
        price = ""
        # moneyType = li.xpath('.//div[@class="col-price"]/p[@class="prc"]/span[1]/i[1]/text()')[0]
        if li.xpath('.//div[@class="flight-seats-list"]/div[@class="flight-price-row flight-price-row-h2"]/span[@class="col-seat-price"]/span[@class="price-info flight-total-price price-lower-info"]/text()'):
           price = li.xpath('.//div[@class="flight-seats-list"]/div[@class="flight-price-row flight-price-row-h2"]/span[@class="col-seat-price"]/span[@class="price-info flight-total-price price-lower-info"]/text()')[0]
        elif li.xpath('.//div[@class="flight-seats-list"]/div[@class="flight-price-row flight-price-row-h2"]/span[@class="col-seat-price"]/span[@class="price-info flight-total-price"]/text()'):
           price = li.xpath('.//div[@class="flight-seats-list"]/div[@class="flight-price-row flight-price-row-h2"]/span[@class="col-seat-price"]/span[@class="price-info flight-total-price"]/text()')[0]
        elif li.xpath('.//div[@class="flight-seats-list"]/div[@class="flight-price-row flight-price-row-h1"]/span[@class="col-seat-price"]/span[@class="price-info flight-total-price price-lower-info"]/text()'):
           price = li.xpath('.//div[@class="flight-seats-list"]/div[@class="flight-price-row flight-price-row-h1"]/span[@class="col-seat-price"]/span[@class="price-info flight-total-price price-lower-info"]/text()')[0]
        else:
           price = li.xpath('.//div[@class="flight-seats-list"]/div[@class="flight-price-row flight-price-row-h1"]/span[@class="col-seat-price"]/span[@class="price-info flight-total-price"]/text()')[0]

        if li.xpath('.//div[@class="flight-seats-list"]/div[@class="flight-price-row flight-price-row-h2"]/span[@class="col-seat-price"]/text()'):
            moneyType = li.xpath(
                './/div[@class="flight-seats-list"]/div[@class="flight-price-row flight-price-row-h2"]/span[@class="col-seat-price"]/text()')[0]
        else:
            moneyType = li.xpath('.//div[@class="flight-seats-list"]/div[@class="flight-price-row flight-price-row-h1"]/span[@class="col-seat-price"]/text()')[0]

        print(price)
        ticket_discount = ""
        if li.xpath('.//div[@class="flight-seats-list"]/div[@class="flight-price-row flight-price-row-h1"]/span[@class="col-seat-status"]/text()'):
            ticket_discount = li.xpath('.//div[@class="flight-seats-list"]/div[@class="flight-price-row flight-price-row-h1"]/span[@class="col-seat-status"]/text()')[0]
        # 保存到MySQL数据库
        self.save(air_company, air_type, date, start_time, end_time, duration, start_station,
                  transit_airport_title, transit_airport_city, transit_airport, transit_airport_time,
                  transit_airport_duration, end_station, moneyType, price, ticket_discount, "tuniu")

    def save(self, air_company, air_type, dep_date, dep_time, arr_time, duration, dep_airport, transit_airport_title, transit_airport_city,
             transit_airport, transit_airport_time, transit_airport_duration, arr_airport, ticket_price_type, ticket_price, ticket_discount, ticket_resource):
        with self.connection.cursor() as cursor:
            sql = 'INSERT INTO qunaer_flight_info(air_company, air_type, dep_date, dep_time, arr_time, duration, dep_airport, transit_airport_title, transit_airport_city, transit_airport, transit_airport_time, transit_airport_duration, arr_airport, ticket_price_type, ticket_price, ticket_discount, ticket_resource, dep_city, arr_city) ' \
                  'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

            sql2 = "update qunaer_flight_info set ticket_price = '%s'where dep_date='%s' and air_type = '%s' and air_company='%s' and dep_time='%s'" % (ticket_price, dep_date, air_type, air_company, dep_time)
            cursor.execute(
                "select * from qunaer_flight_info where dep_date='%s' and air_type = '%s' and air_company='%s' and dep_time='%s' and arr_time = '%s'" % (dep_date, air_type, air_company, dep_time, arr_time))
            lists = cursor.fetchall()
            if lists:
                cursor.execute(sql2)
            else:
                cursor.execute(sql, (air_company, air_type, dep_date, dep_time, arr_time, duration, dep_airport, transit_airport_title, transit_airport_city, transit_airport,
                                    transit_airport_time, transit_airport_duration, arr_airport, ticket_price_type, ticket_price, ticket_discount, ticket_resource, self.depCity, self.arrCity))
        self.connection.commit()



if __name__ == '__main__':
    i = 15
    while i < 20:
        url = 'http://flight.tuniu.com/intel'
        spider = TrainTicketSpider(depCity="上海", arrCity="洛杉矶", depdate="2018-07-"+str(i))
        # spider = TrainTicketSpider(depCity=sys.argv[1], arrCity=sys.argv[2], depdate=sys.argv[3])
        spider.crawl(url)
        print("第%d天爬取结束" % i)
        i += 1
        time.sleep(5)