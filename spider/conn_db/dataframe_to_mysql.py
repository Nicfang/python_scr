#!/usr/bin/env python
#  -*- coding: utf-8 -*-

import os, sys
import pandas as pd
import time, datetime, calendar
import send_mail
import conn_db

reload(sys)
sys.setdefaultencoding('utf8')


class dataframe_to_mysql():


    def get_mysql_data(self,conn, sql):

        mysql_data = pd.read_sql(sql, conn)
        count = len(mysql_data.index)
        print 'has %s record' % count
        return mysql_data
        conn.close()

    # 插入数据到mysql
    def cnn_sql(self,conn, sql):
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            conn.commit()
            print u'更新成功'
        except Exception, e:
            conn.rollback()
            print u'未更新'
            print e
            return e

    def insert_to_mysql(self, df,table, columns_list, start_col, end_col):

        '''
        :param df: 插入的数据 dataframe
        :param columns_list: mysql表列名
        :param start_col,end_col: DUPLICATE key --除主键外的值
        :return:
        '''

        c = tuple(map(lambda x: x.encode('gb2312').replace("'", ''), columns_list))
        c = str(c).replace("'", '')

        for k in df.values:
            o = ""
            for j in k:
                o = o + "'" + str(j) + "'" + ","
            o = o[:-1]

            update_str = ''
            for z in range(start_col, end_col):
                p = str(columns_list[z]) + "= '" + str(k[z]) + "',"
                update_str += p
            update_str = update_str[:-1]
            sql = 'insert INTO '+ str(table) + ' '+ str(c) + ' VALUES (' + o + ') on DUPLICATE key UPDATE ' + update_str
            yield sql

    def butch_insert_to_mysql(self,df, table, columns_list, start_col, end_col,conn,error_subject_table_name):

        '''
        :param df: 插入的数据 dataframe
        :param table: 插入的表名 数据库+表名 string
        :param columns_list: mysql表列名 list
        :param start_col,end_col: DUPLICATE key --除主键外的值
        :param conn: 数据库连接 mysql_connect.conn?
        :param error_subject_table_name: 报错时的表名（中文）string
        :return:Void
        '''

        c = tuple(map(lambda x: x.encode('gb2312').replace("'", ''), columns_list))
        c = str(c).replace("'", '')

        num = 5000
        page = [w for w in range(len(df) + 1) if w % num == 0]
        if page[0] != 0:
            page[0] = 0
        if page[-1] != len(df):
            page.append(len(df) + 1)
        print  page

        for p in range(len(page) - 1):
            print page[p], page[p + 1]
            new_df = df[page[p]:page[p + 1]]
            insert_butch_sql = ''
            for k in new_df.values:
                o = ""
                for j in k:
                    o = o + "'" + str(j) + "'" + ","
                o = o[:-1]

                update_str = ''
                for z in range(start_col, end_col):
                    p = str(columns_list[z]) + "= '" + str(k[z]) + "',"
                    update_str += p
                update_str = update_str[:-1]
                sql = 'insert INTO ' + str(table) + ' ' + str(
                    c) + ' VALUES (' + o + ') on DUPLICATE key UPDATE ' + update_str + ';\n'
                insert_butch_sql = insert_butch_sql + sql

            error_msg = dataframe_to_mysql().cnn_sql(conn, insert_butch_sql)
            if error_msg >= 5:
                send_mail.Mailer(to_list=['1261592462@qq.com'], new_df=None, th1=error_subject_table_name+u'表sql插入报错！',
                                 Subject=u'sql插入报错！', unipath=None)
            print u'--------------Done!----------------'


    def insert_to_mysql_flow(self,table, columns_list,value_list, start_col, end_col,conn):

        '''

        :param table: 数据库表名
        :param columns_list: 列名list
        :param value_list: value值list
        :param start_col: 确定唯一替换开始位置
        :param end_col: 确定唯一替换介绍位置
        :param conn: 链接数据库
        :return:
        '''

        c = tuple(map(lambda x: x.encode('gb2312').replace("'", ''), columns_list))
        c = str(c).replace("'", '')

        o = ""
        for j in value_list:
            o = o + "'" + str(j) + "'" + ","
        o = o[:-1]

        update_str = ''
        for z in range(start_col, end_col):
            p = str(columns_list[z]) + "= '" + str(value_list[z]) + "',"
            update_str += p
        update_str = update_str[:-1]
        sql = 'insert INTO '+ str(table) + ' '+ str(c) + ' VALUES (' + o + ') on DUPLICATE key UPDATE ' + update_str+';'
        print sql
        dataframe_to_mysql().cnn_sql(conn, sql)

