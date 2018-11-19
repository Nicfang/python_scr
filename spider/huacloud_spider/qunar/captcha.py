#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import urllib2
import urllib
import time
from io import BytesIO
from PIL import Image
from form import register


def main(api_key):
    captcha = CaptchaAPI(api_key)
    print register('Test Account', 'Test Account', 'example125@webscraping.com', 'example', captcha.solve)


class CaptchaError(Exception):
    pass


class CaptchaAPI:
    def __init__(self, api_key, timeout=60):
        self.api_key = api_key
        self.timeout = timeout
        self.url = 'https://www.9kw.eu/index.cgi'


    def solve(self, img):
        """Submit CAPTCHA and return result when ready
        """
        img_buffer = BytesIO()
        img.save(img_buffer, format="PNG")
        img_data = img_buffer.getvalue()
        captcha_id = self.send(img_data)##发送验证码到该API
        start_time = time.time()
        while time.time() < start_time + self.timeout:
            try:
                text = self.get(captcha_id)##获取验证码图像处理结果
            except CaptchaError:
                pass # CAPTCHA still not ready
            else:
                if text != 'NO DATA':
                    if text == 'ERROR NO USER':
                        raise CaptchaError('Error: no user available to solve CAPTCHA')
                    else:
                        print 'CAPTCHA solved!'
                        print "验证码为 ：",text
                        return text
            print 'Waiting for CAPTCHA ...'
        raise CaptchaError('Error: API timeout')


    def send(self, img_data):
        """Send CAPTCHA for solving
        发送验证码到该API
        """
        print 'Submitting CAPTCHA'
        data = {
            'action': 'usercaptchaupload',
            'apikey': self.api_key,
            'file-upload-01': img_data.encode('base64'),
            'base64': '1',
            '''
            'selfsolve': '1':表示如果我们正在使用9kw的Web界面处理验证码，那么验证码图像会传给我们自己处理
             如果我们没有处于登录，那么会将验证码图像传给其他用户处理
            '''
            'selfsolve': '1',
            'maxtimeout': str(self.timeout)
        }
        encoded_data = urllib.urlencode(data)
        request = urllib2.Request(self.url, encoded_data)
        response = urllib2.urlopen(request)
        result = response.read()
        self.check(result)
        return result


    def get(self, captcha_id):
        """Get result of solved CAPTCHA
        获取验证码图像处理结果
        """
        data = {
            'action': 'usercaptchacorrectdata',
            'id': captcha_id,
            'apikey': self.api_key,
            'info': '1'
        }
        encoded_data = urllib.urlencode(data)
        response = urllib2.urlopen(self.url + '?' + encoded_data)
        result = response.read()
        self.check(result)
        return result


    def check(self, result):
        """Check result of API and raise error if error code detected
        该方法只检查初始字符，确认其是否遵循错误信息前包含4位数字错误码的格式。
        """
        if re.match('00\d\d \w+', result):
            raise CaptchaError('API error: ' + result)

if __name__ == '__main__':
        api_key = '1FLYJ8B8035NQM9K12'
        main(api_key)