#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymysql
from dataframe_to_mysql import dataframe_to_mysql
import send_mail
# 本地数据库

conn_localhost = pymysql.connect(host='localhost', port=3306, user='root', passwd='sa123456',db='online_db', charset='utf8')

