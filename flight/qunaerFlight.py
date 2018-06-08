# !/usr/bin/env python
# -*- coding:utf-8 -*-
import time
import pymysql
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class TrainTicketSpider(object):
    """
    使用Selenium库和PhantomJS浏览器,爬取去哪儿网机票信息
    只实现当日单程票查询
    """

    def __init__(self):
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36")
        self.browser = webdriver.PhantomJS(
            executable_path=r"C:\Users\pyin\AppData\Local\Programs\Python\Python36-32\Scripts\phantomjs-2.1.1-windows\phantomjs-2.1.1-windows\bin\phantomjs.exe")

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

        #单程还是往返
        searchType = self.browser.find_element_by_id("searchTypeSng")

        #始发地
        fromCity = self.browser.find_element_by_name("fromCity")

        #目的地
        toCity = self.browser.find_element_by_name("toCity")

        #出发时间
        date = self.browser.find_element_by_id("fromDate")

        #搜索按钮
        searchBtn = self.browser.find_element_by_class_name("btn_search")

        # searchType.clear()
        # searchType.click()

        fromCity.clear()
        # fromCity.send_keys(input('输入发车站>> '))
        fromCity.send_keys("北京")
        fromCity.click()

        toCity.clear()
        # toCity.send_keys(input('请输入目的地>>'))
        toCity.send_keys("上海")
        toCity.click()

        date.clear()
        # date.send_keys(input('输入车车日期(格式:2000-01-22)>> '))
        date.send_keys("2018-06-16")
        date.click()

        searchBtn.click()

        time.sleep(3)
        self.browser.save_screenshot('2.png')

        self.parse(current_page=1)

    def parse(self, current_page):
        html = self.browser.page_source
        HTML = etree.HTML(html)

        #获取页数
        # pages = HTML.xpath('//div[@class="main"]/div[@class="content"]/div[@class="m-page"]/div[@class="container"]/a[@data-pager-pageno]/text()')
        pages = HTML.xpath('//a[@class="page"]/text()')
        page_count = len(pages) + 1

        # fly_list = self.browser.find_element_by_class_name("b-airfly")
        fly_list = HTML.xpath('//div[@class="mb-10"]/div[@class="m-airfly-lst"]/div')
        # fly_list = HTML.xpath('//div[@class="main"]/div[@class="content"]/div[@data-reactid=".1.2"]/div[@data-reactid=".1.2.3"]/div[@class="mb-10"]/div[@class="m-airfly-lst"]/div')

        for li in fly_list:
            # 航空公司/类型
            fly_com = li.xpath('.//div[@class="e-airfly"]/div[@class="col-trip"]/div[@class="s-trip"]/div[@class="col-airline"]/div[@class="d-air"]/div[@class="air"]/span/text()')[0].strip('\n ')
            fly_type = li.xpath('.//div[@class="num"]/span[1]/text()')[0] + li.xpath('.//div[@class="num"]/span[2]/text()')[0]
            fly_info = fly_com + fly_type
            print('正在获取飞机型号>>>', fly_info)

            # 发站/到站
            print(li.xpath('.//div[@class="sep-lf"]/p[@class="airport"]/span/text()')[0])
            # print(li.xpath('.//div[@class="sep-lf"]/p[@class="airport"]/span/text()')[1])
            start_station = li.xpath('.//div[@class="sep-lf"]/p[@class="airport"]/span/text()')[0]
            end_station = li.xpath('.//div[@class="sep-rt"]/p[@class="airport"]/span/text()')[0]

            STATION = (start_station + '-' + end_station).strip('\n ')

            # 发站时间/到站时间
            start_time = li.xpath('.//div[@class="sep-lf"]/h2/text()')[0]
            end_time = li.xpath('.//div[@class="sep-rt"]/h2/text()')[0]
            TIME = (start_time + '-' + end_time).strip('\n ')

            # 运行时间
            DURATION = li.xpath('.//div[@class="range"]/text()')[0].strip('\n ')

            # 参考票价
            PRICE = ""
            moneyType = li.xpath('.//div[@class="col-price"]/p[@class="prc"]/span[1]/i[1]/text()')[0]
            # ticket_body = li.xpath('.//div[@class="col-price"]/span[@class="prc_wp"]/em[@class="rel"]')[0]  # 车票类型列表
            # old_ticket_price = li.xpath('.//div[@class="col-price"]/p[@class="prc"]/span[1]/span[@class="prc_wp"]/em[@class="rel"]/b[1]/i/text()')
            update_ticket_price = li.xpath('.//div[@class="col-price"]/p[@class="prc"]/span[1]/span[1]/span[1]/em[@class="rel"]/b[1]/i/text()')
            # new_price = li.xpath('.//div[@class="col-price"]/p[@class="prc"]/span[1]/span[1]/span[1]/em[@class="rel"]/b/text()')

            new_price_first = ""
            if li.xpath('.//div[@class="col-price"]/p[@class="prc"]/span[1]/span[1]/span[1]/em[@class="rel"]/b[@style="width: 18px;left:-18px"]/text()'):
                new_price_first = li.xpath(
                    './/div[@class="col-price"]/p[@class="prc"]/span[1]/span[1]/span[1]/em[@class="rel"]/b[@style="width: 18px;left:-18px"]/text()')[0]

            new_price_second = ""
            if li.xpath('.//div[@class="col-price"]/p[@class="prc"]/span[1]/span[1]/span[1]/em[@class="rel"]/b[@style="width: 18px;left:-36px"]/text()'):
                new_price_second = li.xpath(
                    './/div[@class="col-price"]/p[@class="prc"]/span[1]/span[1]/span[1]/em[@class="rel"]/b[@style="width: 18px;left:-36px"]/text()')[0]

            new_price_three = ""
            if li.xpath('.//div[@class="col-price"]/p[@class="prc"]/span[1]/span[1]/span[1]/em[@class="rel"]/b[@style="width: 18px;left:-54px"]/text()'):
                new_price_three = li.xpath(
                    './/div[@class="col-price"]/p[@class="prc"]/span[1]/span[1]/span[1]/em[@class="rel"]/b[@style="width: 18px;left:-54px"]/text()')[0]

            new_price_four = ""
            if li.xpath('.//div[@class="col-price"]/p[@class="prc"]/span[1]/span[1]/span[1]/em[@class="rel"]/b[@style="width: 18px;left:-72px"]/text()'):
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

            for i in update_ticket_price:
                PRICE = PRICE + str(i)

            # 保存到MySQL数据库
            self.save(fly_info, STATION, TIME, DURATION, PRICE)

        # 如果有下一页,点击下一页按钮,继续爬取
        page_count -= current_page
        if page_count:
            current_page += 1
            a_next = self.browser.find_element(By.XPATH, '//a[@data-pager-pageno={page}]'.format(page=current_page))
            a_next.click()
            time.sleep(3)

            # 递归调用解析方法
            self.parse(current_page)
        else:
            print('爬取结束')
            # 关闭数据库
            self.connection.close()

    def save(self, Fly_info, station, time, duration, PRICE):
        with self.connection.cursor() as cursor:
            sql = 'INSERT INTO qunaer(train_num,station,time,duration,price_nums) VALUES (%s,%s,%s,%s,%s)'
            cursor.execute(sql, (Fly_info, station, time, duration, PRICE))
        self.connection.commit()

if __name__ == '__main__':
    url = 'https://flight.qunar.com'
    spider = TrainTicketSpider()
    spider.crawl(url)


