# !/usr/bin/env python
# -*- coding:utf-8 -*-
import time
import pymysql
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
import sys

class TrainTicketSpider(object):
    """
    使用Selenium库和PhantomJS浏览器,爬取去哪儿网机票信息
    只实现当日单程票查询
    """

    def __init__(self, depCity, arrCity, depdate):
        self.depCity = depCity
        self.arrCity = arrCity
        self.depDate = depdate
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = (
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36")
        dcap["phantomjs.page.settings.loadImages"] = False
        self.browser = webdriver.PhantomJS(
            executable_path=r"C:\Users\pyin\AppData\Local\Programs\Python\Python36-32\Scripts\phantomjs-2.1.1-windows\phantomjs-2.1.1-windows\bin\phantomjs.exe",
            desired_capabilities=dcap, service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'])
        # chrome_options = Options()
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--disable-gpu')
        # chrome_options.add_argument("window-size=1024,768")
        # chrome_options.add_argument("--no-sandbox")
        # self.browser = webdriver.Chrome("C:\chromedriver\chromedriver.exe", chrome_options=chrome_options)
        # self.browser = webdriver.Chrome("/opt/flight/chromedriver.exe", chrome_options=chrome_options)
        self.connection = pymysql.connect(host='localhost',
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

        # searchType = self.browser.find_elements_by_class_name("input_radio")[0]

        # 始发地
        fromCity = self.browser.find_element_by_id("J_FormDepartCity")

        # 目的地
        toCity = self.browser.find_element_by_id("J_FormDestCity")

        # 出发时间
        jsString = "document.getElementById('J_FormDepartDate').removeAttribute('readonly')"
        self.browser.execute_script(jsString)
        date = self.browser.find_element_by_id("J_FormDepartDate")

        # 搜索按钮
        searchBtn = self.browser.find_element_by_id("J_Search")

        # aaa = self.browser.find_element_by_id("cui_hd")

        # searchType.click()

        fromCity.clear()
        fromCity.send_keys(self.depCity)
        # fromCity.click()
        #time.sleep(0.5)

        toCity.clear()
        toCity.send_keys(self.arrCity)
        toCity.click()
        time.sleep(0.5)

        date.clear()
        # date.click()
        date.send_keys(self.depDate)
        time.sleep(0.5)

        # aaa.click()
        searchBtn.click()
        time.sleep(5)
        z = self.browser.window_handles
        print(z)
        #self.browser.switch_to.window(self.browser.window_handles[1])
        # self.browser.switch_to_window(self.browser.window_handles[1])
        self.browser.save_screenshot('2.png')

        self.parse(current_page=1, date=self.depDate)

    def parse(self, current_page, date):
        html = self.browser.page_source
        HTML = etree.HTML(html)

        print(HTML)
        fly_list = HTML.xpath('//div[@class="flightlist"]/div')

        for li in fly_list:
            self.getData(li, date)

        print('爬取结束')
        # 关闭数据库
        self.connection.close()
        self.browser.quit()

    def getData(self, li, date):
        # 航空公司/类型
        air_company = li.xpath('.//div[@class="J-flightlist"]/div[@class="J-flight"]/div[@class="J-flightDetail"]/div[1]/div[@class="fl-logo"]/ul/li[@class="fl-airInf"]/div[@class="right"]/div[@class="aircom"]/text()')[0]
        air_type_arr = li.xpath('.//div[@class="J-flightlist"]/div[@class="J-flight"]/div[@class="J-flightDetail"]/div[1]/div[@class="fl-logo"]/ul/li[@class="fl-airInf"]/div[@class="right"]/div[2]/a[@class="infoWrapper"]/div[@class="flihtnumber left"]/span/text()')
        air_type = air_type_arr[0] + air_type_arr[1]
        fly_info = air_company + air_type
        print('正在获取飞机型号>>>', fly_info)

        # 起飞机场/到达机场/图转机场
        start_station_arr = li.xpath('.//div[@class="J-flightlist"]/div[@class="J-flight"]/div[@class="J-flightDetail"]/div[2]/div[@class="fl-depart"]/div[@class="fl-departInf"]/p[@class="airport"]/text()')
        start_station = ""
        for i in start_station_arr:
            start_station += i

        end_station_arr = li.xpath('.//div[@class="J-flightlist"]/div[@class="J-flight"]/div[@class="J-flightDetail"]/div[4]/div[@class="fl-arrive"]/div[@class="fl-arriveInf"]/p[@class="airport"]/span/text()')
        end_station = ""
        for j in end_station_arr:
            end_station += j



        transit_airport_title = ""
        transit_airport_city = ""
        transit_airport = ""
        transit_airport_time = ""
        transit_airport_duration = ""
        if li.xpath('.//div[@class="J-flightlist"]/div[@class="J-flight"]/div[@class="J-flightDetail"]/div[3]/div[@class="fl-center"]/a/p[@class="durationTransfer"]/span/text()'):
            transit_airport_city = li.xpath('.//div[@class="J-flightlist"]/div[@class="J-flight"]/div[@class="J-flightDetail"]/div[3]/div[@class="fl-center"]/a/p[@class="durationTransfer"]/span/text()')[0]


        STATION = (start_station + '-' + end_station).strip('\n ')

        # 起飞时间/到达时间
        start_time = li.xpath('.//div[@class="J-flightlist"]/div[@class="J-flight"]/div[@class="J-flightDetail"]/div[2]/div[@class="fl-depart"]/div[@class="fl-departInf"]/p[@class="hours"]/text()')[0]
        end_time = li.xpath('.//div[@class="J-flightlist"]/div[@class="J-flight"]/div[@class="J-flightDetail"]/div[4]/div[@class="fl-arrive"]/div[@class="fl-arriveInf"]/span[@class="hours"]/span/text()')[0]

        # 飞行时间
        duration = li.xpath('.//div[@class="J-flightlist"]/div[@class="J-flight"]/div[@class="J-flightDetail"]/div[3]/div[@class="fl-center"]/p[@class="durationTime"]/text()')[0].strip('\n ')

        # 参考票价
        price = ""
        # moneyType = li.xpath('.//div[@class="col-price"]/p[@class="prc"]/span[1]/i[1]/text()')[0]
        price = li.xpath('.//div[@class="J-flightlist"]/div[@class="J-right"]/div[@class="J-priceWrap"]/div[@class="price"]/div[@class="wrapper"]/span[@class="num"]/text()')[0]
        moneyType = li.xpath('.//div[@class="J-flightlist"]/div[@class="J-right"]/div[@class="J-priceWrap"]/div[@class="price"]/div[@class="wrapper"]/span[@class="yuan"]/text()')[0]

        ticket_discount = li.xpath('.//div[@class="J-flightlist"]/div[@class="J-right"]/div[@class="J-priceWrap"]/div[@class="price"]/div[@class="child_ticket"]/text()')[0]
        # 保存到MySQL数据库
        self.save(air_company, air_type, date, start_time, end_time, duration, start_station,
                  transit_airport_title, transit_airport_city, transit_airport, transit_airport_time,
                  transit_airport_duration, end_station, moneyType, price, ticket_discount, "tuniu")

    def save(self, air_company, air_type, dep_date, dep_time, arr_time, duration, dep_airport, transit_airport_title, transit_airport_city,
             transit_airport, transit_airport_time, transit_airport_duration, arr_airport, ticket_price_type, ticket_price, ticket_discount, ticket_resource):
        with self.connection.cursor() as cursor:
            sql = 'INSERT INTO qunaer_flight_info(air_company, air_type, dep_date, dep_time, arr_time, duration, dep_airport, transit_airport_title, transit_airport_city, transit_airport, transit_airport_time, transit_airport_duration, arr_airport, ticket_price_type, ticket_price, ticket_discount, ticket_resource, dep_city, arr_city) ' \
                  'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            cursor.execute("select * from qunaer_flight_info where dep_date='%s' and air_type = '%s' and dep_time = '%s'" % (dep_date, air_type, dep_time))
            lists = cursor.fetchall()
            if lists:
                pass
            else:
                cursor.execute(sql, (air_company, air_type, dep_date, dep_time, arr_time, duration, dep_airport, transit_airport_title, transit_airport_city, transit_airport,
                                    transit_airport_time, transit_airport_duration, arr_airport, ticket_price_type, ticket_price, ticket_discount, ticket_resource, self.depCity, self.arrCity))
        self.connection.commit()



if __name__ == '__main__':
    url = 'http://flight.tuniu.com/intel'
    spider = TrainTicketSpider(depCity="上海", arrCity="三亚", depdate="2018-11-23")
    # spider = TrainTicketSpider(depCity=sys.argv[1], arrCity=sys.argv[2], depdate=sys.argv[3])
    spider.crawl(url)