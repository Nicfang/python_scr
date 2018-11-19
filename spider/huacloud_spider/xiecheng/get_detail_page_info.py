#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
__author__ = 'Nic fang'
__time__   = '2018/6/15'
__description__   = ''
'''
import datetime
import multiprocessing
import random
import re

import conn_db
from selenium import webdriver
import time
from bs4 import BeautifulSoup
# from multiprocessing import Pool

import sys
reload(sys)
sys.setdefaultencoding('utf8')

class get_detail_page_info:

    def __init__(self):

        self.sql = 'select hotel_id,hotel_url from online_db.spider_xiecheng_data where logitude is NULL group by hotel_id'
        self.mysql_db_table = 'online_db.spider_xiecheng_data'

    def get_url(self):

        url_data = conn_db.dataframe_to_mysql().get_mysql_data(conn=conn_db.conn_localhost,sql=self.sql)
        url_data = url_data.sample(frac=1).reset_index(drop=True)
        # print url_data.head()
        return url_data

    def get_detail_data(self):

        try:
            hotel_urls = get_detail_page_info().get_url()
            driver=webdriver.PhantomJS(executable_path=r'D:\Python27\phantomjs\phantomjs-2.1.1-windows\bin\phantomjs.exe')
            a = 0
            for hotel_id,url in hotel_urls.values:
                try:
                    today = datetime.datetime.today()+ datetime.timedelta(days=random.randint(1,3))
                    start = str(datetime.datetime.strftime( today , '%Y-%m-%d'))
                    end = str(datetime.datetime.strftime( today + datetime.timedelta(days=random.randint(0,8)), '%Y-%m-%d'))
                    url = url.replace('2018-06-16',start).replace('2018-06-17',end)
                    print url
                    driver.get(url)
                    time.sleep(2)
                    # driver.set_page_load_timeout(10)
                    times=10
                    for i in range(times + 1):
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(2)

                    pageSource=driver.page_source
                    soup = BeautifulSoup(pageSource, "html.parser")
                    if soup:
                        hotel_mobile = soup.find('span', attrs={'id': 'J_realContact'}).get('data-real')
                        hotel_mobile = re.findall(r'\(?0\d{2,3}[) -]?\d{7,8}|1\d{10}',str(hotel_mobile))
                        hotel_mobile = '|'.join(hotel_mobile)

                        # hotel_position = soup.find('iframe', attrs={'frameborder': '0'}).get('fakesrc')
                        # logitude = re.search("shxLongitude=\d+(\.\d+)?",hotel_position).group().split('=')[-1]
                        # latitude = re.search("shxLatitude=\d+(\.\d+)?",hotel_position).group().split('=')[-1]
                        logitude = soup.find('meta', attrs={'itemprop': 'longitude'}).get('content')
                        latitude = soup.find('meta', attrs={'itemprop': 'latitude'}).get('content')
                        print(hotel_id,hotel_mobile,logitude,latitude)
                        colum_name = ['hotel_id','hotel_mobile','logitude','latitude']
                        value_list = [hotel_id if hotel_id else '',hotel_mobile if hotel_mobile else '',
                                      logitude if logitude else '',latitude if latitude else '']
                        if hotel_id:
                            conn_db.dataframe_to_mysql().update_to_mysql_flow(self.mysql_db_table,
                                                                                'hotel_id',hotel_id,colum_name,
                                                                              value_list,conn_db.conn_localhost)
                    a+=1
                    if a%20 ==0:
                        driver.close()
                        driver=webdriver.PhantomJS(executable_path=r'D:\Python27\phantomjs\phantomjs-2.1.1-windows\bin\phantomjs.exe')
                except Exception,e:
                    print e
            driver.close()
        except Exception,e:
            print e

if __name__ == '__main__':

    for i in range(4):
        p = multiprocessing.Process(target=get_detail_page_info().get_detail_data, args=())
        p.start()
