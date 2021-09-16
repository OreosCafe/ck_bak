# -*- coding: utf-8 -*-
"""
cron: 1 15 * * *
new Env('恩山论坛');
"""

import os, re, requests, time
from utils import get_data
from mtr_notify import send


class EnshanCheckIn:
    def __init__(self, enshan_cookie_list):
        self.enshan_cookie_list = enshan_cookie_list


    def sign(self, cookie):
        url = 'https://www.right.com.cn/FORUM/home.php?mod=spacecp&ac=credit&showcredit=1'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
            'Cookie': cookie
        }
        session = requests.session()
        resp = session.get(url, headers=headers)
        try:
            coin = re.findall('恩山币: </em>(.*?)nb &nbsp;', resp.text)[0]
            point = re.findall('<em>积分: </em>(.*?)<span', resp.text)[0]
            result = f'恩山币：{coin}\n积分：{point}'
        except Exception as e:
            result = str(e)
        return result


    def main(self):
        msg_all = ""
        i = 1
        for enshan_cookie in self.enshan_cookie_list:
            cookie = str(enshan_cookie.get("enshan_cookie"))
            result = self.sign(cookie=cookie)
            msg = f'账号{i}' + '\n------ 签到结果 ------\n' + result
            time.sleep(1)
            i += 1
            msg_all += msg + '\n\n'
        return msg_all


if __name__ == '__main__':
    data = get_data()
    _enshan_cookie_list = data.get("ENSHAN_COOKIE_LIST", [])
    res = EnshanCheckIn(enshan_cookie_list=_enshan_cookie_list).main()
    print(res)
    send("恩山论坛", res)