#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib,urllib2
import json
from pandas.io.json import json_normalize
import pandas as pd
import time
import os,sys
import requests
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')

files = 'report'+ time.strftime('%m-%d',time.localtime(time.time()))
path = unicode( '/data/script/daily/' + files,encoding='utf-8')
isExists=os.path.exists(path)
if not isExists:
    os.makedirs(path)
    print str(path) + '创建成功'
else:
    print str(path)+'目录已存在'

def request_info(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(unicode(response.content), 'lxml')
        return soup
    except Exception, e:
        print Exception, e

def base_site_info():

    try:
        url = 'http://m.to8to.com/html/index.html'
        soup = request_info(url)
        spell = soup.select('#cityPage > div.city_info > section > div > ul > a')
        name = soup.select('#cityPage > div.city_info > section > div > ul > a > li ')

        city_spell = []
        city_name = []
        for i in spell:
            city_spell.append(i.get('href').replace('/',''))
        for i in name:
            city_name.append(i.text)
        return city_spell,city_name

    except Exception, e:
        print Exception, e

def get_company_id(url):
    try:
        soup2 = request_info(url)
        company_url2 = soup2.select('body > ul.company-list > li > a')
        for x in company_url2:
            x = x.get('href')
            return x
    except Exception, e:
        print Exception, e

def company_url(city_spell):

    try:
        url = 'http://m.to8to.com/'+str(city_spell)+'/company/'
        soup = request_info(url)
        page_num = soup.find(attrs={'class':'widget-pagination-current-page'})
        url_list = []
        if page_num is None:
            a = url
            a = get_company_id(a)
            print(a)
            url_list.append(a)
        else:
            page_num = page_num.text.split('/')[-1]
            for i in range(1,int(page_num)+1):
                a = '%slist_%s.html/' % (url,i)
                a = get_company_id(a)
                a = 'http://m.to8to.com/'+str(a)
                print(a)
                url_list.append(a)
        return url_list

    except Exception, e:
        print Exception, e

def get_info(url):

    try:
        soup= request_info(url)

        company_names = soup.select('body > div.topbannerFrame.top-banner-remove.mar-95 > figure > div > h1')
        addresses = soup.select('#addressDown > span')
        mobiles = soup.select('body > div.topbannerFrame.top-banner-remove.mar-95 > figure > div > a')
        a = []
        for company_name,address,mobile in zip(company_names,addresses,mobiles):
            company_name = company_name.text
            address = address.text
            mobile = mobile.get('href').split(':')[-1]
            a.append(company_name)
            a.append(address)
            a.append(mobile)
        print(a)
        return a
    except Exception, e:
        print Exception, e


# def base_url1(page=None,num=None,cityname=None):
#
#     url1 = 'https://mobileapi.to8to.com/index.php?action=listV2_1&appid=15&appostype=2&appversion=5.0.0&channel=appstore&cityName=%E6%88%90%E9%83%BD&idfa=0edc9d0b-eb60-4f4e-98d5-6d95a7872b06&latitude=30.6693322&longitude=103.998102&model=company&page=' +str(page) + '&paging=true&perPage=' +str(num) + '&systemversion=10.3.3&t8t_device_id=D9E002E2-16BF-4FC6-AA67-AF97768E7030&to8to_token=&townId=0&type=3&uid=0&version=2.5&withCase=1'
#     return url1
#
# def base_url2(page=None,num=None,cityname=None):
#
#     url2 = 'http://m.to8to.com/cd/zs/1172406/#from=app'
#
#     return url2
#
# def base_info(url = None):
#
#     response = urllib2.Request(url)
#
#     response = urllib2.urlopen(response)
#     response = response.read()
#
#     print(response)
#     return response
#
#
#
# def get_json_info(data):
#
#     data = json.loads(data)
#     data = data['data']
#     df = json_normalize(data)
#     print(df)
#     return df


if __name__ == '__main__':

    # url1 = base_url1(page=1,num=1000)
    # a = base_info(url1)
    # df1 = get_json_info(a)
    #
    # filenames = u'土巴兔数据' + time.strftime('%m-%d',time.localtime(time.time())) + '.xlsx'
    # unipath = path + '/' + filenames
    # writer = pd.ExcelWriter(unipath)
    # df1.to_excel(writer,unicode('土巴兔数据','utf-8'))
    #
    # writer.save()

    # city_spell,city_name = base_site_info()
    # df1 = pd.DataFrame(data=[city_spell,city_name]).T.ix[30:,:]
    # df1.columns = columns=['spell','name']
    # url_list = []
    # for i in df1.spell:
    #     print(i)
    #     url = company_url(i)
    #     url_list.extend(url)
    # print url_list

    company_url = company_url('bj')
    for x in company_url:
        print x
        get_info(x)




