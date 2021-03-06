#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
#import urllib2
import time

from bs4 import BeautifulSoup
import datetime
import random
#import urlparse
#service_args=['--proxy=127.0.0.1:9150','--proxy-type=socks5',]
import conn_db


class yilong_spider:

    def __init__(self):
        self.mysql_db_table = 'online_db.spider_yilong_data'

    def random_date(self):

            start = datetime.datetime.today() + datetime.timedelta(days=random.randint(1,24))
            start_date = str(datetime.datetime.strftime(start, '%Y-%m-%d'))
            end_date = str(datetime.datetime.strftime(start +  datetime.timedelta(days=random.randint(0,5)), '%Y-%m-%d'))
            return start_date

    # driver=webdriver.Firefox()

    # date = random_date()
    # print('---------------------')
    # driver.find_element_by_xpath("//input[@id='inDate']").send_keys(date)
    # time.sleep(5)
    # pageSource=driver.page_source
    # print(pageSource)

    def get_base_info(self):

        driver=webdriver.PhantomJS(executable_path=r'D:\python2.7\phantomjs\bin\phantomjs.exe')

        driver.get('http://hotel.elong.com/chengdu/')
        time.sleep(2)
        page=0
        hotels_inf=[]
        while page<=580:
            times=10
            for i in range(times + 1):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(5)
            pageSource=driver.page_source
            # html=pageSource.decode("utf-8")
            soup = BeautifulSoup(pageSource, "html.parser")
            if soup:
                hotel_info = soup.findAll('span', attrs={'class': 'l1'})

                for x in hotel_info:
                    hotel_name = x.get('title')
                    logitude = x.get('data-lng')
                    latitude = x.get('data-lat')
                    hotel_id = x.get('data-hotelid')
                    hotel_address = x.get('data-hoteladdress')
                    print hotel_id,hotel_name,logitude,latitude,hotel_address
                    colum_name = ['hotel_id','hotel_name','hotel_address','logitude','latitude']
                    value_list = [hotel_id if hotel_id else '',hotel_name if hotel_name else '',
                                  hotel_address if hotel_address else '',logitude if logitude else '',
                                  latitude if latitude else '']
                    if hotel_name:
                        conn_db.dataframe_to_mysql().insert_to_mysql_flow(self.mysql_db_table,colum_name,value_list
                                                ,0,len(colum_name)-1,conn_db.conn_localhost)

            print '---------------------------------------------------------------'
            driver.find_element_by_xpath("//a[contains(text(),'下一页')]").click() # selenium的xpath用法，找到包含“下一页”的a标签去点击
            page = page + 1
            time.sleep(2) # 睡2秒让网页加载完再去读它的html代码
            # with open(date+".txt","w") as f:
            #     for hotel_inf in hotels_inf:
            #         for hotel_attr in hotel_inf:
            #             print hotel_attr
            #             f.write(hotel_attr.encode('utf8')+' ')
            #         f.write('\n')
        # driver.get('http://hotel.elong.com/chengdu/')
        # time.sleep(2)
        driver.close()

if __name__ == '__main__':

    yilong_spider().get_base_info()