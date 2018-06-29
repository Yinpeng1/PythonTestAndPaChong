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
        self.browser = webdriver.Chrome("C:\chromedriver\chromedriver.exe", chrome_options=chrome_options)
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
        self.browser.save_screenshot('1.png')

        searchType = self.browser.find_elements_by_class_name("input_radio")[0]

        # 始发地
        fromCity = self.browser.find_element_by_id("homeCity")

        # 目的地
        toCity = self.browser.find_element_by_id("destCity")

        # 出发时间
        date = self.browser.find_element_by_id("DDate")

        # 搜索按钮
        searchBtn = self.browser.find_element_by_id("searchBtn")

        aaa = self.browser.find_element_by_id("cui_hd")

        searchType.click()

        fromCity.clear()
        fromCity.send_keys(self.depCity)
        fromCity.click()
        time.sleep(0.5)

        toCity.clear()
        toCity.send_keys(self.arrCity)
        toCity.click()
        time.sleep(0.5)

        date.clear()
        date.send_keys(self.depDate)
        date.click()
        time.sleep(0.5)

        aaa.click()
        searchBtn.click()
        time.sleep(2)
        self.browser.save_screenshot('2.png')

        self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(3)
        self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(3)
        self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(2)
        self.browser.execute_script('window.scrollTo(document.body.scrollHeight, 0)')

        self.parse(current_page=1, date=self.depDate)

    def parse(self, current_page, date):
        html = self.browser.page_source
        HTML = etree.HTML(html)

        fly_list = HTML.xpath('//div[@id="flightList"]/div')

        if fly_list:
            for li in fly_list:
                if li.xpath('.//div[@class="flight-item   "]'):
                    li = li.xpath('.//div[@class="flight-item   "]')
                    # print(len(li))
                    for i in li:
                        self.getData(i, date)
                else:
                    if li.xpath('.//div[@class="flight-row"]'):
                        self.getData(li, date)
                    else:
                        continue
        else:
            fly_list = HTML.xpath('.//div[@id="J_flightlist2"]/div')
            for li in fly_list:
                if li.xpath('.//div[@class="search_transfer_title"]'):
                    continue
                elif li.xpath('.//div[@class="search_more_transfer_city_inner"]'):
                    pass
                elif li.xpath('.//div[@class="search_transfer_tab"]/a/h3/text()'):
                    pass
                else:
                    self.getZNDate(li, date)

        print('爬取结束')
        # 关闭数据库
        self.connection.close()

    def getZNDate(self, li, date):
        if li.xpath('.//div[@class="near_flt_header"]'):
            print("nihao")
        elif li.xpath('.//div[@class="search_transfer_header J_header_row J_header_wrap"]'):
            air_company1 = li.xpath('.//div[@class="inb logo"]/div[1]/span/strong/text()')[0]
            air_company2 = li.xpath('.//div[@class="inb logo"]/div[2]/span/strong/text()')[0]
            air_company = air_company1 + ", " + air_company2
            air_type1 = li.xpath('.//div[@class="inb logo"]/div[1]/span/span/text()')[0]
            air_type2 = li.xpath('.//div[@class="inb logo"]/div[2]/span/span/text()')[0]
            # li.xpath('.//table/tbody/tr/td[@class="logo"]/div[@class="low_text"]/span/text()')[0]
            air_type = air_type1 + ", "+ air_type2
            fly_info = air_company1 + air_type1 + "--" + air_company2 + air_type2
            print('正在获取飞机型号>>>', fly_info)

            start_time = li.xpath('.//div[@class="inb right"]/div[1]/strong/text()')[0]

            start_station = li.xpath('.//div[@class="inb right"]/div[2]/text()')[0]

            end_time = li.xpath('.//div[@class="inb left"]/div[1]/strong/text()')[0]

            end_station = li.xpath('.//div[@class="inb left"]/div[2]/text()')[0]

            duration = ""
            transit_airport_title = ""
            transit_airport_city = ""
            transit_airport = ""
            transit_airport_time = ""
            transit_airport_duration = ""
            if li.xpath('.//div[@class="inb center J_trans_pop"]'):
                transit_airport_city = li.xpath('.//div[@class="inb center J_trans_pop"]/span[@class="stay-city"]/span/text()')[0]
                transit_airport_duration = li.xpath('.//div[@class="inb center J_trans_pop"]/span[@class="stay-time"]/text()')[0]

            moneyType = li.xpath('.//div[@class="inb price  "]/span[@class="base_price02 J_base_price"]/dfn/text()')[0]
            price = li.xpath('.//div[@class="inb price  "]/span[@class="base_price02 J_base_price"]/text()')[0]
            ticket_discount = li.xpath(
                './/div[@class="inb price  "]/div[@class="child_ticket"]/span[@class="low_text"]/text()')[0]

            # 保存到MySQL数据库
            self.save(air_company, air_type, date, start_time, end_time, duration, start_station,
                      transit_airport_title, transit_airport_city, transit_airport, transit_airport_time,
                      transit_airport_duration, end_station, moneyType, price, ticket_discount, "xiecheng")
        else:
            air_company = li.xpath('.//table/tbody/tr/td[@class="logo"]/div[@class="clearfix J_flight_no"]/strong/text()')[0]

            if li.xpath('.//table/tbody/tr/td[@class="logo"]/div[@class="low_text"]/span/text()'):
                air_type = li.xpath('.//table/tbody/tr/td[@class="logo"]/div[@class="clearfix J_flight_no"]/span/text()')[0] + \
                           li.xpath('.//table/tbody/tr/td[@class="logo"]/div[@class="low_text"]/span/text()')[0]
            else:
                air_type = li.xpath('.//table/tbody/tr/td[@class="logo"]/span/text()')[0]
            fly_info = air_company + air_type
            print('正在获取飞机型号>>>', fly_info)

            start_time = li.xpath(
                 './/table[@class="search_table_header"]/tbody/tr/td[@class="right"]/div/strong/text()')[0]

            start_station = li.xpath('.//table[@class="search_table_header"]/tbody/tr/td[@class="right"]/div/text()')[0]

            end_time = li.xpath('.//table[@class="search_table_header"]/tbody/tr/td[@class="left"]/div/strong/text()')[0]
            end_station = li.xpath('.//table[@class="search_table_header"]/tbody/tr/td[@class="left"]/div/text()')[0]

            duration=""
            transit_airport_title = ""
            transit_airport_city = ""
            transit_airport = ""
            transit_airport_time = ""
            transit_airport_duration = ""
            if li.xpath('.//table[@class="search_table_header"]/tbody/tr/td[@class="center"]/div[@class="stopover"]'):
                transit_airport_city = li.xpath('.//table[@class="search_table_header"]/tbody/tr/td[@class="center"]/div[@class="stopover"]/text()')[0] + \
                                       li.xpath('.//table[@class="search_table_header"]/tbody/tr/td[@class="center"]/div[@class="stopover"]/span/text()')[0]

            moneyType = "¥"

            if li.xpath('.//table[@class="search_table_header"]/tbody/tr/td[@class="price lowest_price "]/span[@class="J_base_price"]/span[@class="base_price02"]/text()'):
                price = li.xpath('.//table[@class="search_table_header"]/tbody/tr/td[@class="price lowest_price "]/span[@class="J_base_price"]/span[@class="base_price02"]/text()')[0]
            else:
                price = li.xpath('.//table[@class="search_table_header"]/tbody/tr/td[@class="price "]/span[@class="J_base_price"]/span[@class="base_price02"]/text()')[0]

            if li.xpath('.//table[@class="search_table_header"]/tbody/tr/td[@class="price lowest_price "]/div[@class="child_ticket"]/text()'):
                ticket_discount = li.xpath('.//table[@class="search_table_header"]/tbody/tr/td[@class="price lowest_price "]/div[@class="child_ticket"]/span/text()')[0]
            else:
                ticket_discount = li.xpath('.//table[@class="search_table_header"]/tbody/tr/td[@class="price "]/div[@class="child_ticket"]/span[@class="low_text"]/text()')[0]

            # 保存到MySQL数据库
            self.save(air_company, air_type, date, start_time, end_time, duration, start_station,
                      transit_airport_title, transit_airport_city, transit_airport, transit_airport_time,
                      transit_airport_duration, end_station, moneyType, price, ticket_discount, "xiecheng")



    def getData(self, li, date):
        # 航空公司/类型
        s = li.xpath('.//div[@class="flight-row"]/div[@class="flight-col-base"]/div[@class="airline-name"]/strong[@class="base-airline"]/text()')
        t = li.xpath('.//div[@class="flight-row"]/div[@class="flight-col-base"]/div[@class="airline-name"]/span[@class="extra-airline"]/text()')
        if s or t:
            air_company = s[0] + t[0]
        else:
            air_company = li.xpath('.//div[@class="flight-row"]/div[@class="flight-col-base"]/div[@class="airline-name"]/text()')[0].strip('\n ')


        if li.xpath('.//div[@class="flight-row"]/div[@class="flight-col-base"]/div[@class="flight-No"]/span[@class="plane-type"]/span[@class="abbr"]/text()'):
            air_type = li.xpath('.//div[@class="flight-row"]/div[@class="flight-col-base"]/div[@class="flight-No"]/text()')[0] + \
            li.xpath('.//div[@class="flight-row"]/div[@class="flight-col-base"]/div[@class="flight-No"]/span[@class="plane-type"]/span[@class="abbr"]/text()')[0]
        else:
            air_type = li.xpath('.//div[@class="flight-row"]/div[@class="flight-col-base"]/div[@class="flight-No"]/text()')[0]
        if air_type == "2程航班":
            air_type = li.xpath('.//div[@class="flight-detail-section"]/p[@class="section-flight-base"]/span[@class="flight-No"]/text()')[0] + \
                       li.xpath('.//div[@class="flight-detail-section"]/p[@class="section-flight-base"]/span[@class="plane-type"]/span[@class="abbr"]/text()')[0]

        fly_info = air_company + air_type
        print('正在获取飞机型号>>>', fly_info)

        # 起飞机场/到达机场/图转机场
        if li.xpath('.//div[@class="flight-row"]/div[@class="flight-col-detail"]/div[@class="flight-detail-depart"]/div[@class="flight-detail-airport"]/span/text()'):
            start_station = li.xpath(
                './/div[@class="flight-row"]/div[@class="flight-col-detail"]/div[@class="flight-detail-depart"]/div[@class="flight-detail-airport"]/text()')[0] + \
                            li.xpath(
                                './/div[@class="flight-row"]/div[@class="flight-col-detail"]/div[@class="flight-detail-depart"]/div[@class="flight-detail-airport"]/span/text()')[
                                0]
        else:
            start_station = li.xpath(
                './/div[@class="flight-row"]/div[@class="flight-col-detail"]/div[@class="flight-detail-depart"]/div[@class="flight-detail-airport"]/text()')[0]

        if li.xpath('.//div[@class="flight-row"]/div[@class="flight-col-detail"]/div[@class="flight-detail-return"]/div[@class="flight-detail-airport"]/span/text()'):
            end_station = li.xpath('.//div[@class="flight-row"]/div[@class="flight-col-detail"]/div[@class="flight-detail-return"]/div[@class="flight-detail-airport"]/text()')[0] + \
                          li.xpath(
                              './/div[@class="flight-row"]/div[@class="flight-col-detail"]/div[@class="flight-detail-return"]/div[@class="flight-detail-airport"]/span/text()')[0]
        else:
            end_station = li.xpath('.//div[@class="flight-row"]/div[@class="flight-col-detail"]/div[@class="flight-detail-return"]/div[@class="flight-detail-airport"]/text()')[0]



        transit_airport_title = ""
        transit_airport_city = ""
        transit_airport = ""
        transit_airport_time = ""
        transit_airport_duration = ""
        if li.xpath(
                './/div[@class="flight-row"]/div[@class="flight-col-more"]/div[@class="flight-stop-info"]/div[@class="flight-stop"]/span[@class="stop-city stop-city-transfer"]/text()'):
            # print(len(li.xpath('.//div[@class="trans"]/div[@class="g-up-tips"]/span[@class="t"]/span/text()')))
            transit_airport_city = li.xpath('.//div[@class="flight-row"]/div[@class="flight-col-more"]/div[@class="flight-stop-info"]/div[@class="flight-stop"]/span[@class="stop-city stop-city-transfer"]/text()')[0]

        if li.xpath('.//div[@class="flight-detail-expend"]/div[@class="section-stop"]/div[@class="in"]/text()'):
            transit_airport_duration = li.xpath('.//div[@class="flight-detail-expend"]/div[@class="section-stop"]/div[@class="in"]/text()')[0]

        STATION = (start_station + '-' + end_station).strip('\n ')

        # 起飞时间/到达时间
        start_time = li.xpath(
            './/div[@class="flight-row"]/div[@class="flight-col-detail"]/div[@class="flight-detail-depart"]/div[@class="flight-detail-time"]/text()')[
            0]
        end_time = li.xpath(
            './/div[@class="flight-row"]/div[@class="flight-col-detail"]/div[@class="flight-detail-return"]/div[@class="flight-detail-time"]/text()')[
            0]
        TIME = (start_time + '-' + end_time).strip('\n ')

        # 飞行时间
        duration = \
        li.xpath('.//div[@class="flight-row"]/div[@class="flight-col-more"]/div[@class="flight-total-time"]/text()')[
            0].strip('\n ')

        # 参考票价
        price = ""
        # moneyType = li.xpath('.//div[@class="col-price"]/p[@class="prc"]/span[1]/i[1]/text()')[0]
        price = li.xpath(
            './/div[@class="seats-list"]/div[@class="seat-row    "]/div[@class="seat-price"]/div[1]/div[@class="mb5"]/span[2]/text()')[0]
        moneyType = li.xpath(
            './/div[@class="seats-list"]/div[@class="seat-row    "]/div[@class="seat-price"]/div[1]/div[@class="mb5"]/span[2]/dfn/text()')[0]

        # 保存到MySQL数据库
        self.save(air_company, air_type, date, start_time, end_time, duration, start_station,
                  transit_airport_title, transit_airport_city, transit_airport, transit_airport_time,
                  transit_airport_duration, end_station, moneyType, price, "", "xiecheng")

    def save(self, air_company, air_type, dep_date, dep_time, arr_time, duration, dep_airport, transit_airport_title, transit_airport_city,
             transit_airport, transit_airport_time, transit_airport_duration, arr_airport, ticket_price_type, ticket_price, ticket_discount, ticket_resource):
        with self.connection.cursor() as cursor:
            sql = 'INSERT INTO qunaer_flight_info(air_company, air_type, dep_date, dep_time, arr_time, duration, dep_airport, transit_airport_title, transit_airport_city, transit_airport, transit_airport_time, transit_airport_duration, arr_airport, ticket_price_type, ticket_price, ticket_discount, ticket_resource, dep_city, arr_city) ' \
                  'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            sql2 = "update qunaer_flight_info set ticket_price = '%s' where dep_date='%s' and air_type = '%s' and air_company='%s' and dep_time='%s'" % (ticket_price, dep_date, air_type,air_company, dep_time)
            cursor.execute("select * from qunaer_flight_info where dep_date='%s' and air_type = '%s' and air_company='%s' and dep_time='%s'" % (dep_date, air_type,air_company, dep_time))
            lists = cursor.fetchall()
            if lists:
                cursor.execute(sql2)
            else:
                cursor.execute(sql, (air_company, air_type, dep_date, dep_time, arr_time, duration, dep_airport, transit_airport_title, transit_airport_city, transit_airport,
                                    transit_airport_time, transit_airport_duration, arr_airport, ticket_price_type, ticket_price, ticket_discount, ticket_resource, self.depCity, self.arrCity))
        self.connection.commit()



if __name__ == '__main__':
    url = 'http://flights.ctrip.com/international/'
    spider = TrainTicketSpider(depCity="上海", arrCity="香港", depdate="2018-07-28")
    # spider = TrainTicketSpider(depCity=sys.argv[1], arrCity=sys.argv[2], depdate=sys.argv[3])
    spider.crawl(url)