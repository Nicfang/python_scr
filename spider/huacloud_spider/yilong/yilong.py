#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import re
import time
import os,sys
import requests
from bs4 import BeautifulSoup
import random
from time import sleep
import datetime
import conn_db

reload(sys)
sys.setdefaultencoding('utf-8')

class qunar_spider:

    def __init__(self):

         self.n = 35000
         self.mysql_db_table= 'online_db.spider_qunar_data'

         self.user_agents=[
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
        "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
    ]

    def get_proxy_ip(self):

        sql = 'select proxy_ip,port,get_fun from online_db.proxy_ip_info'
        proxy_info = conn_db.dataframe_to_mysql().get_mysql_data(conn=conn_db.conn_localhost,sql=sql)
        proxy_ip = []
        for proxy,port,get_fun in proxy_info.values:
            proxy_dic = u"http://"+str(proxy)+u":"+str(port)
            proxy_dic = {get_fun:proxy_dic}
            proxy_ip.append(proxy_dic)
        return proxy_ip


     #下载页面 如果没法下载就 等待1秒 再下载
    def download_soup_waitting(self,url,proxies):
        try:
            # proxies = [{'http':'42.227.161.53:32480'}
            #          ,{'http':'60.168.11.156:40421'},{'http':'219.131.250.173:44028'}
            #          ,{'http':'114.237.28.130:39011'},{'http':'114.237.63.90:49696'}]

            # #创建ProxyHandler
            # proxy_support = request.ProxyHandler(proxy[2])
            # #创建Opener
            # opener = request.build_opener(proxy_support)
            # response = requests.get(url, headers=headers, proxies=proxies)

            headers = { 'User-Agent': random.choice(self.user_agents),
                        # 'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/201002201 Firefox/55.0',
                        # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        # 'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                        # 'Accept-Encoding': 'gzip, deflate, br',
                        # 'Cookie': '',
                        # 'Connection': 'keep-alive',
                        # 'Pragma': 'no-cache',
                        # 'Cache-Control': 'no-cache'
                        }

            s = requests.Session()
            response= s.get(url,headers=headers,timeout=10
                            ,proxies = proxies
                            )
            print('response_code:'+str(response.status_code))
            print(response.content)
            if response.status_code==200:
                html=response.content
                html=html.decode("utf-8")
                soup = BeautifulSoup(html, "html.parser")
                return soup
            else:
                time.sleep(random.random()*3)
                print("等待ing")

            return qunar_spider().download_soup_waitting(url)

        except Exception,e:
            print(e)
            return ""

    def get_hotel_id(self):

        sql_hotel_sql = 'select hotel_id from online_db.spider_qunar_data group by hotel_id'
        sql_hotel_id = conn_db.dataframe_to_mysql().get_mysql_data(conn=conn_db.conn_localhost,sql=sql_hotel_sql)
        sql_hotel_id = [x for x in sql_hotel_id.values]
        hotel_id = [i for i in range(1,self.n) if i not in sql_hotel_id]
        random.shuffle(hotel_id)
        return hotel_id

    def get_detail_info(self,url,hotel_id,proxy):

        soup = qunar_spider().download_soup_waitting(url,proxy)
        if soup:

            hotel_info = soup.find('div', attrs={'class': 'hotel-info-left'})
            hotel_name = hotel_info.find('h1').text

            hotel_address = soup.find('div', attrs={'class': 'text-overflow qt-lh hotel-address'})
            if hotel_address:
                hotel_address = hotel_address.text
            else:
                hotel_address = ''

            location = hotel_info.find('h1').get('data-gpoint')
            if location:
                logitude = location.split(',')[0]
                latitude = location.split(',')[1]
            else:
                logitude = ''
                latitude = ''

            hotel_info = soup.find('div', attrs={'class': 'text-overflow qt-lh'}).findAll('span')

            print(hotel_info)
            if hotel_info:
                    pattern = re.findall(r'\(?0\d{2,3}[) -]?\d{7,8}|1\d{10}',str(hotel_info))
                    if pattern:
                        hotel_mobile = '|'.join(pattern)
                    else:
                        hotel_mobile = ''
            else:
                hotel_mobile = ''

            colum_name = ['hotel_id','hotel_name','hotel_address','logitude','latitude','hotel_mobile']
            value_list = [hotel_id,hotel_name,hotel_address,logitude,latitude,hotel_mobile]
            if hotel_name:
                conn_db.dataframe_to_mysql().insert_to_mysql_flow(self.mysql_db_table,colum_name,value_list
                                        ,0,len(colum_name),conn_db.conn_localhost)

    def random_date(self):

        start = datetime.datetime.today() + datetime.timedelta(days=random.randint(0,5))
        start_date = str(datetime.datetime.strftime(start, '%Y-%m-%d'))
        end_date = str(datetime.datetime.strftime(start +  datetime.timedelta(days=random.randint(0,5)), '%Y-%m-%d'))
        return start_date,end_date

if __name__ == '__main__':

    #获取酒店id-list
    hotel_list = qunar_spider().get_hotel_id()
    ####获取代理ip-list
    proxies = qunar_spider().get_proxy_ip()

    for hotel_id in hotel_list:

        #获取随机url参数
        ran_int_3 = str(random.randint(100,999))
        ran_int_4 = ran_int_3+str(random.randint(0,9))
        ran_int_5 = ran_int_4+str(random.randint(0,9))

        #获取最近随机日期
        start_date,end_date = qunar_spider().random_date()

        print(hotel_id)
        url = str("http://touch.qunar.com/hotel/hoteldetail?cityUrl=chengdu&checkInDate="+str(start_date)+"&"
                  "checkOutDate="+str(end_date)+"&seq=chengdu_"+str(hotel_id)
                  +"&isLM=0&extra=%"+ran_int_3+"B%"+ran_int_4+"th%+ran_int_4+%"+ran_int_3+"A%"+ran_int_4+"fx_PREFERENTIAL%"
                  +ran_int_4+"%"+ran_int_3+"C%"+ran_int_4+"%"+ran_int_4+"%"+ran_int_3+"A%"+ran_int_5+"%"+ran_int_4+"%"+ran_int_3+"D"
            )
        proxy = random.choice(proxies)
        print(proxy)
        print(url)
        qunar_spider().get_detail_info(url=url,
                                       hotel_id=hotel_id,
                                       proxy=proxy)
        sleep(random.randint(3,8))

