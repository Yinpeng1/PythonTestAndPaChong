# !/usr/bin/env python
# -*- coding:utf-8 -*-
import time
import pymysql
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
import redis
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
            desired_capabilities=dcap)

        self.connection = pymysql.connect(host='localhost',
                                          user='root',
                                          password='123',
                                          db='test',
                                          port=3306,
                                          charset='utf8',  # 不能用utf-8

                                          cursorclass=pymysql.cursors.DictCursor)

    def crawl(self, url):
        self.browser.set_page_load_timeout(30)
        try:
            self.browser.get(url)
        except:
            pass
        self.browser.save_screenshot('1.png')

        # 单程还是往返
        # searchType = self.browser.find_element_by_id("searchTypeSng")

        # 始发地
        fromCity = self.browser.find_element_by_name("fromCity")

        # 目的地
        toCity = self.browser.find_element_by_name("toCity")

        # 出发时间
        date = self.browser.find_element_by_id("fromDate")

        # 搜索按钮
        searchBtn = self.browser.find_element_by_class_name("btn_search")

        # searchType.clear()
        # searchType.click()

        fromCity.clear()
        # fromCity.send_keys(input('输入发车站>> '))
        fromCity.send_keys(self.depCity)
        time.sleep(1)
        fromCity.click()

        toCity.clear()
        # toCity.send_keys(input('请输入目的地>>'))
        toCity.send_keys(self.arrCity)
        time.sleep(1)
        toCity.click()

        date.clear()
        # nowDate = input('输入车车日期(格式:2000-01-22)>> ')
        date.send_keys(self.depDate)
        # date.send_keys("2018-06-23")
        time.sleep(1)
        date.click()
        self.browser.save_screenshot('2.png')

        searchBtn.click()
        time.sleep(5)
        # time.sleep(50)
        self.browser.save_screenshot('2.png')

        self.parse(current_page=1, date=self.depDate)

    def parse(self, current_page, date):
        html = self.browser.page_source
        HTML = etree.HTML(html)

        # 获取页数
        pages = HTML.xpath('//a[@class="page"]/text()')
        page_count = len(pages) + 1

        fly_list = HTML.xpath('//div[@class="mb-10"]/div[@class="m-airfly-lst"]/div')

        for li in fly_list:
            # 航空公司/类型
            air_company = li.xpath(
                './/div[@class="e-airfly"]/div[@class="col-trip"]/div[@class="s-trip"]/div[@class="col-airline"]/div[@class="d-air"][1]/div[@class="air"]/span/text()')[0].strip('\n ')

            # print(len(li.xpath('.//div[@class="e-airfly"]/div[@class="col-trip"]/div[@class="s-trip"]/div[@class="col-airline"]/div[@class="d-air"]')))
            # if len(li.xpath('.//div[@class="e-airfly"]/div[@class="col-trip"]/div[@class="s-trip"]/div[@class="col-airline"]/div[@class="d-air"]')) == 2:
            #     air_type = li.xpath('.//div[@class="num"][1]/span[1]/text()')[0] + li.xpath('.//div[@class="num"][1]/span[2]/text()')[0] + ',' + li.xpath('.//div[@class="num"][2]/span[1]/text()')[0] + li.xpath('.//div[@class="num"][2]/span[2]/text()')[0]
            air_type = li.xpath('.//div[@class="num"]/span[1]/text()')[0] + li.xpath('.//div[@class="num"]/span[2]/text()')[0]
            fly_info = air_company + air_type
            print('正在获取飞机型号>>>', fly_info)

            # 起飞机场/到达机场/图转机场
            # print(li.xpath('.//div[@class="sep-lf"]/p[@class="airport"]/span/text()')[0])
            if len(li.xpath('.//div[@class="sep-lf"]/p[@class="airport"]/span/text()')) == 2:
                start_station = li.xpath('.//div[@class="sep-lf"]/p[@class="airport"]/span/text()')[0] + li.xpath('.//div[@class="sep-lf"]/p[@class="airport"]/span/text()')[1]
            else:
                start_station = li.xpath('.//div[@class="sep-lf"]/p[@class="airport"]/span/text()')[0]

            if len(li.xpath('.//div[@class="sep-rt"]/p[@class="airport"]/span/text()')) == 2:
                end_station = li.xpath('.//div[@class="sep-rt"]/p[@class="airport"]/span/text()')[0] + li.xpath('.//div[@class="sep-rt"]/p[@class="airport"]/span/text()')[1]
            else:
                end_station = li.xpath('.//div[@class="sep-rt"]/p[@class="airport"]/span/text()')[0]

            transit_airport_title = ""
            transit_airport_city = ""
            transit_airport = ""
            transit_airport_time = ""
            transit_airport_duration = ""
            transit_airport_info = ""
            if li.xpath('.//div[@class="trans"]/div[@class="g-up-tips"]/span[@class="t"]/span/text()'):
                print(len(li.xpath('.//div[@class="trans"]/div[@class="g-up-tips"]/span[@class="t"]/span/text()')))
                if len(li.xpath('.//div[@class="trans"]/div[@class="g-up-tips"]/span[@class="t"]/span/text()')) == 2:
                    transit_airport_title = li.xpath('.//div[@class="trans"]/div[@class="g-up-tips"]/span[@class="t"]/span/text()')[0] + li.xpath('.//div[@class="trans"]/div[@class="g-up-tips"]/span[@class="t"]/span/text()')[1]
                if li.xpath('.//div[@class="trans"]/div[@class="g-up-tips"]/span[@class="t"]/span/text()')[0] == "转":
                    transit_airport = li.xpath('.//div[@class="trans"]/div[@class="g-up-tips"]/div[@class="m-tips"]/div[@class="b-tips b-tips-nowrap"]/div[@class="e-tipscont"]/div[1]/div[@class="seg-ct"]/p/span/text()')
                    for i in transit_airport:
                        transit_airport_info += str(i)
                        transit_airport_duration = li.xpath('.//div[@class="trans"]/div[@class="g-up-tips"]/div[@class="m-tips"]/div[@class="b-tips b-tips-nowrap"]/div[@class="e-tipscont"]/div[1]/div[@class="seg-ct"]/p[@class="seg transfer"]/span[1]/span[2]/text()')[0]



            STATION = (start_station + '-' + end_station).strip('\n ')

            # 起飞时间/到达时间
            start_time = li.xpath('.//div[@class="sep-lf"]/h2/text()')[0]
            end_time = li.xpath('.//div[@class="sep-rt"]/h2/text()')[0]
            TIME = (start_time + '-' + end_time).strip('\n ')

            # 飞行时间
            duration = li.xpath('.//div[@class="range"]/text()')[0].strip('\n ')

            # 参考票价
            price = ""
            moneyType = li.xpath('.//div[@class="col-price"]/p[@class="prc"]/span[1]/i[1]/text()')[0]
            update_ticket_price = li.xpath(
                './/div[@class="col-price"]/p[@class="prc"]/span[1]/span[1]/span[1]/em[@class="rel"]/b[1]/i/text()')
            ticket_discount = li.xpath('.//div[@class="col-price"]/div[@class="vim"]/span/text()')[0]
            update_ticket_price = self.update_price(update_ticket_price, li)
            for i in update_ticket_price:
                price = price + str(i)

            # 保存到MySQL数据库
            self.save(air_company, air_type, date, start_time, end_time, duration, start_station,
                      transit_airport_title, transit_airport_city, transit_airport_info, transit_airport_time,
                      transit_airport_duration, end_station, moneyType, price, ticket_discount, "qunaer")

        # 如果有下一页,点击下一页按钮,继续爬取
        page_count -= current_page
        if page_count:
            current_page += 1
            a_next = self.browser.find_element(By.XPATH, '//a[@data-pager-pageno={page}]'.format(page=current_page))
            a_next.click()
            time.sleep(3)

            # 递归调用解析方法
            self.parse(current_page, date=date)
        else:
            print('爬取结束')
            # 关闭数据库
            self.connection.close()


    def update_price(self, update_ticket_price, li):
        new_price_first = ""
        if li.xpath(
                './/div[@class="col-price"]/p[@class="prc"]/span[1]/span[1]/span[1]/em[@class="rel"]/b[@style="width: 18px;left:-18px"]/text()'):
            new_price_first = li.xpath(
                './/div[@class="col-price"]/p[@class="prc"]/span[1]/span[1]/span[1]/em[@class="rel"]/b[@style="width: 18px;left:-18px"]/text()')[0]

        new_price_second = ""
        if li.xpath(
                './/div[@class="col-price"]/p[@class="prc"]/span[1]/span[1]/span[1]/em[@class="rel"]/b[@style="width: 18px;left:-36px"]/text()'):
            new_price_second = li.xpath(
                './/div[@class="col-price"]/p[@class="prc"]/span[1]/span[1]/span[1]/em[@class="rel"]/b[@style="width: 18px;left:-36px"]/text()')[0]

        new_price_three = ""
        if li.xpath(
                './/div[@class="col-price"]/p[@class="prc"]/span[1]/span[1]/span[1]/em[@class="rel"]/b[@style="width: 18px;left:-54px"]/text()'):
            new_price_three = li.xpath(
                './/div[@class="col-price"]/p[@class="prc"]/span[1]/span[1]/span[1]/em[@class="rel"]/b[@style="width: 18px;left:-54px"]/text()')[0]

        new_price_four = ""
        if li.xpath(
                './/div[@class="col-price"]/p[@class="prc"]/span[1]/span[1]/span[1]/em[@class="rel"]/b[@style="width: 18px;left:-72px"]/text()'):
            new_price_four = li.xpath(
                './/div[@class="col-price"]/p[@class="prc"]/span[1]/span[1]/span[1]/em[@class="rel"]/b[@style="width: 18px;left:-72px"]/text()')[0]
        if len(update_ticket_price) == 3:
            if new_price_three:
                update_ticket_price[0] = new_price_three
            if new_price_second:
                update_ticket_price[1] = new_price_second
            if new_price_first:
                update_ticket_price[2] = new_price_first
        if len(update_ticket_price) == 4:
            if new_price_four:
                update_ticket_price[0] = new_price_four
            if new_price_three:
                update_ticket_price[1] = new_price_three
            if new_price_second:
                update_ticket_price[2] = new_price_second
            if new_price_first:
                update_ticket_price[3] = new_price_first
        return update_ticket_price

    # def get_transit_airport_info(self):

    def save(self, air_company, air_type, dep_date, dep_time, arr_time, duration, dep_airport, transit_airport_title, transit_airport_city,
             transit_airport, transit_airport_time, transit_airport_duration, arr_airport, ticket_price_type, ticket_price, ticket_discount, ticket_resource):
        with self.connection.cursor() as cursor:
            sql = 'INSERT INTO qunaer_flight_info(air_company, air_type, dep_date, dep_time, arr_time, duration, dep_airport, transit_airport_title, transit_airport_city, transit_airport, transit_airport_time, transit_airport_duration, arr_airport, ticket_price_type, ticket_price, ticket_discount, ticket_resource, dep_city, arr_city) ' \
                  'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            cursor.execute(sql, (air_company, air_type, dep_date, dep_time, arr_time, duration, dep_airport, transit_airport_title, transit_airport_city, transit_airport,
                                transit_airport_time, transit_airport_duration, arr_airport, ticket_price_type, ticket_price, ticket_discount, ticket_resource, self.depCity, self.arrCity))
        self.connection.commit()


if __name__ == '__main__':
    url = 'https://flight.qunar.com'
    spider = TrainTicketSpider(depCity="上海", arrCity="三亚", depdate="2018-10-26")
    # spider = TrainTicketSpider(depCity=sys.argv[1], arrCity=sys.argv[2], depdate=sys.argv[3])
    spider.crawl(url)
