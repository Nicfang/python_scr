#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import socket
import struct

print random.randint(100,999)
import requests

User_Agent=["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36",
"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1","Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 "
                                                                          "Firefox/4.0.1"]
headers = { 'User-Agent': User_Agent[random.randint(0,4)],
# 'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/201002201 Firefox/55.0',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
'Accept-Encoding': 'gzip, deflate, br',
'Cookie': '',
'Connection': 'keep-alive',
'Pragma': 'no-cache',
'Cache-Control': 'no-cache'}

# url = "https://touch.qunar.com/hotel/chengdu/dt-4"
# response= requests.get(url,headers=headers,allow_redirects=False,timeout=5)
# print(response)
import re
hotel_info = '<span>电话028-81238888</span>18782998826'
pattern = re.findall(r'\(?0\d{2,3}[) -]?\d{7,8}|1\d{10}',str(hotel_info))
print(pattern)