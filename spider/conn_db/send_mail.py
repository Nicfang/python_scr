#!/usr/bin/env python
#  -*- coding: utf-8 -*-


import smtplib
import pandas as pd
from email.Header import Header
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
import time


def Mailer(to_list,new_df=None,th1 =None,Subject=None,unipath=None):

    mail_host = 'smtp.exmail.qq.com'
    mail_user = '1261592462@qq.com'
    mail_pwd = 'll543623711'
    s = smtplib.SMTP_SSL(mail_host, 465,timeout=5)
    s.login(mail_user, mail_pwd)

    def HTML_with_style(df, style=None, random_id=None):

        html = '''
                <style>
                    .df thead tr:first-child { background-color: #FF9224; }
                </style>
                ''' + df.to_html(justify='mid', show_dimensions=False, formatters=None, classes='df', index=False)
        return html

    if new_df is None:
        HTML1 = u''
    else:
        HTML1 = HTML_with_style(new_df)


    header = '<html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" /></head>'

    mid = u'<br>' \
          u'<br>'
    body = u'<img width="500" height="120" src="https://hzapp-10006163.image.myqcloud.com/hzapp1510714944" /> <br/>' \
           u'<br>'
    tail = u'Thanks! <br/>' \
           u'Nic Fang<br/>' \
           '</table></body></html>'
    mail = header + th1 + HTML1 + mid + body + tail

    msg = MIMEMultipart()
    msgtext = MIMEText(mail.encode('utf8'), _subtype='html', _charset='utf8')
    msg['From'] = mail_user
    msg['Subject'] = Subject
    msg['To'] = ",".join(to_list)
    # msg['Cc'] = ",".join(cc_list)
    if unipath is not None:
        att1 = MIMEText(open(unipath, 'rb').read(), 'base64', 'gb2312')
        att1["Content-Type"] = 'application/octet-stream'
        att1.add_header('Content-Disposition', 'attachment',filename=(Subject+ '.xlsx').encode('gb2312'))
        msg.attach(att1)
    msg.attach(msgtext)
    print msg['To']
    print msg['Cc']
    try:
        s.sendmail(mail_user, to_list, msg.as_string())
        s.close()
        print '发送成功'
    except Exception, e:
        print e

# if __name__ == '__main__':
#
#     th1 = u't_foreman_recharge_flow、t_foreman_receive_order_flow对比与业务库流水数据，差异如下：' \
#           u'<br>' \
#           u'<br>'
#     Subject = u'注意, 工长技术服务费、流量包、充值流水有异常!'
#     to_list = ['fangb@huizhuang.com']
#     df = pd.DataFrame(columns=['A','B','C','D'])
#
#     Mailer(to_list,df,th1,Subject)
