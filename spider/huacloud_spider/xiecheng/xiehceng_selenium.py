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
import sys


reload(sys)
sys.setdefaultencoding('utf-8')


class yilong_spider:

    def __init__(self):

        self.mysql_db_table = 'online_db.spider_xiecheng_data'

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

        driver=webdriver.PhantomJS(executable_path=r'D:\Python27\phantomjs\phantomjs-2.1.1-windows\bin\phantomjs.exe')

        driver.get('http://hotels.ctrip.com/hotel/chengdu28/')
        time.sleep(2)
        page=0
        while page<=634:
            times=10
            for i in range(times + 1):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                # js="var q=document.body.scrollTop=100000"
                # driver.execute_script(js)
                time.sleep(5)

            pageSource=driver.page_source
            # html=pageSource.decode("utf-8")
            soup = BeautifulSoup(pageSource, "html.parser")
            if soup:
                hotel_info = soup.findAll('li', attrs={'class': 'hotel_item_name'})
                for x in hotel_info:
                    hotel_name_info = x.find('h2', attrs={'class': 'hotel_name'}).find('a')
                    hotel_id = hotel_name_info.get('tracevalue').split(';')[1].replace('hotelid=','')
                    hotel_name = hotel_name_info.get('title')
                    url_ctm = hotel_name_info.get('data-ctm')
                    today = str(datetime.datetime.strftime(datetime.datetime.today() + datetime.timedelta(days=1), '%Y-%m-%d'))
                    hotel_url = 'http://hotels.ctrip.com/'+hotel_name_info.get('href')+'&checkIn'+today+'&checkOut'+today+url_ctm

                    hotel_address_info = x.find('p', attrs={'class': 'hotel_item_htladdress'})
                    hotel_address = hotel_address_info.text.split('。')[0].split('】')[-1]
                    print hotel_id,hotel_name,hotel_url,hotel_address
                    colum_name = ['hotel_id','hotel_name','hotel_url','hotel_address']
                    value_list = [hotel_id if hotel_id else '',hotel_name if hotel_name else '',
                                  hotel_url if hotel_url else '',hotel_address if hotel_address else '']
                    if hotel_name:
                        conn_db.dataframe_to_mysql().insert_to_mysql_flow(self.mysql_db_table,colum_name,value_list
                                                ,0,len(colum_name)-1,conn_db.conn_localhost)

            print '---------------------------------------------------------------'
            driver.find_element_by_xpath("//a[contains(text(),'下一页')]").click() # selenium的xpath用法，找到包含“下一页”的a标签去点击
            page = page + 1
            time.sleep(2)

if __name__ == '__main__':

    yilong_spider().get_base_info()