# !/usr/bin/env python
# -*- coding:utf-8 -*-
import time
import pymysql
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options


class TrainTicketSpider(object):
    """
    使用Selenium库和PhantomJS浏览器,爬取去哪儿网机票信息
    只实现当日单程票查询
    """

    def __init__(self):
        # dcap = dict(DesiredCapabilities.PHANTOMJS)
        # dcap["phantomjs.page.settings.userAgent"] = (
        #     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36")
        # self.browser = webdriver.PhantomJS(
        #     executable_path=r"C:\Users\pyin\AppData\Local\Programs\Python\Python36-32\Scripts\phantomjs-2.1.1-windows\phantomjs-2.1.1-windows\bin\phantomjs.exe")

        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
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

        # 发车站输入框
        # fromStation = self.browser.find_element_b(By.NAME, 'fromStation')
        fromStation = self.browser.find_element_by_name('fromStation')
        # 目的地站输入框
        # toStation = self.browser.find_element(By.NAME, 'toStation')
        toStation = self.browser.find_element_by_name('toStation')
        # 发车日期输入框
        # date = self.browser.find_element(By.NAME, 'date')
        date = self.browser.find_element_by_name('date')
        # 搜索按钮
        # btn_search = self.browser.find_element(By.NAME, 'stsSearch')
        btn_search = self.browser.find_element_by_name('stsSearch')

        aaa = self.browser.find_element_by_class_name("ch_search_tab");

        fromStation.clear()
        fromStation.send_keys(input('输入发车站>> '))
        aaa.click();
        # fromStation.click()
        toStation.clear()
        toStation.send_keys(input('输入目的地站>> '))
        aaa.click();
        # toStation.click()
        date.clear()
        date.send_keys(input('输入车车日期(格式:2000-01-22)>> '))
        aaa.click();
        # date.click()
        btn_search.click()

        time.sleep(3)
        self.browser.save_screenshot('2.png')

        self.parse(current_page=1)

    def parse(self, current_page):
        html = self.browser.page_source
        HTML = etree.HTML(html)

        # 获取页数
        pages = HTML.xpath('//a[@data-pager]/text()')
        page_count = len(pages)

        # 当前页所有车次的元素列表
        li_list = HTML.xpath('//ul[@class="tbody"]/li')

        for li in li_list:
            # 车次/类型
            TRAIN_NUM = li.xpath('.//h3/text()')[0].strip('\n ')

            print('正在获取车次>>>', TRAIN_NUM)

            # 发站/到站
            start_station = li.xpath('.//div[@class="td col2"][1]/p[@class="start"]/span/text()')[0]
            end_station = li.xpath('.//div[@class="td col2"][1]/p[@class="end"]/span/text()')[0]
            STATION = (start_station + '-' + end_station).strip('\n ')

            # 发站时间/到站时间
            start_time = li.xpath('.//div[@class="td col2"][2]/time[@class="startime"]/text()')[0]
            end_time = li.xpath('.//div[@class="td col2"][2]/time[@class="endtime daytime"]/text()')[0]
            TIME = (start_time + '-' + end_time).strip('\n ')

            # 运行时间
            DURATION = li.xpath('.//time[@class="duration"]/text()')[0].strip('\n ')

            # 参考票价
            prices = []
            ticket_types = li.xpath('.//p[@class="ticketed"]/text()')  # 车票类型列表
            ticket_prices = li.xpath('.//span[@class="price"]/text()')  # 车票价格列表
            for type_price in zip(ticket_types, ticket_prices):
                price = '{type} {price}￥'.format(type=type_price[0], price=type_price[1])
                prices.append(price)

            # 剩余票量
            nums = []
            ticket_ps = li.xpath('.//div[@class="td col4"]//p')
            for ticket_p in ticket_ps:
                ticket_num = ticket_p.xpath('./text()')
                if not ticket_num:
                    ticket_num = ticket_p.xpath('./span/text()')
                nums.append(ticket_num)

            # 车票票价和余票数量一一对应
            PRICE_NUMS = ''
            for i in zip(prices, nums):
                price_num = "{}{}".format(i[0], i[1][0])
                PRICE_NUMS = PRICE_NUMS + price_num + ' ,'
            PRICE_NUMS = PRICE_NUMS.strip(',')

            # 保存到MySQL数据库
            self.save(TRAIN_NUM, STATION, TIME, DURATION, PRICE_NUMS)

        # 如果有下一页,点击下一页按钮,继续爬取
        page_count -= current_page
        if page_count:
            current_page += 1
            a_next = self.browser.find_element(By.XPATH, '//a[@data-pager={page}]'.format(page=current_page))
            a_next.click()
            time.sleep(3)

            # 递归调用解析方法
            self.parse(current_page)
        else:
            print('爬取结束')
            # 关闭数据库
            self.connection.close()

    def save(self, train_num, station, time, duration, price_nums):
        """
        保存到MySQL数据库
            create table qunaer(
                id int not null primary key auto_increment,
                train_num varchar(10) not null,
                station varchar(30) not null,
                time varchar(30) not null,
                duration varchar(50) not null,
                price_nums varchar(80) not null,
            );
        """

        with self.connection.cursor() as cursor:
            sql = 'INSERT INTO qunaer(train_num,station,time,duration,price_nums) VALUES (%s,%s,%s,%s,%s)'
            cursor.execute(sql, (train_num, station, time, duration, price_nums))
        self.connection.commit()


if __name__ == '__main__':
    url = 'https://train.qunar.com/'
    spider = TrainTicketSpider()
    spider.crawl(url)
