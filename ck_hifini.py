# -*- coding: utf-8 -*-
"""
cron: 0 0 0 * * *
new Env('HiFiNi');
"""

import re, requests
from utils import get_data
from notify_mtr import send

class HiFiNiCheckIn(object):
    def __init__(self, hifini_cookie_list):
        self.hifini_cookie_list = hifini_cookie_list
        

    def signin(self, cookies):
        sign_in_url = "https://www.hifini.com/sg_sign.htm"
        data = {"x-requested-with": "XMLHttpRequest"}
        cookies = {"enwiki_session":f"{cookies}"}
        r1 = requests.post(url=sign_in_url, data=data, cookies=cookies)
        html_text = r1.text
        is_sign = False
        for line in html_text.splitlines():
            if line.find('今天已经签过啦') != -1:
                msg = "今天已经签过啦"
                is_sign = True
        if not is_sign: msg = "签到成功!"
        return msg


    def main(self):
        msg_all = ''
        i = 1
        for hifini_cookie in self.hifini_cookie_list:
            cookies = hifini_cookie.get('hifini_cookie')
            msg = f'账号{i}\n{self.signin(cookies)}'
            i += 1
            msg_all += msg + '\n\n'
        return msg_all
            

if __name__ == '__main__':
    data = get_data()
    _hifini_cookie_list = data.get("HIFINI_COOKIE_LIST", [])
    res = HiFiNiCheckIn(hifini_cookie_list=_hifini_cookie_list).main()
    print(res)
    send('HiFiNi', res)