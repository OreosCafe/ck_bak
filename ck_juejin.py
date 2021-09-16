# -*- coding: utf-8 -*-
"""
cron: 7 11 * * *
new Env('掘金');
"""

import json, os, requests
from utils import get_data
from mtr_notify import send


class JuejinCheckIn:
    def __init__(self, juejin_cookie_list):
        self.juejin_cookie_list = juejin_cookie_list
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36'}
        self.base_url = 'https://api.juejin.cn/'


    def sign(self, cookie):
        sign_url = self.base_url + 'growth_api/v1/check_in'
        res = requests.post(url=sign_url, headers=self.headers, cookies={'Cookie': cookie}).content
        res = json.loads(res)
        return res


    def lottery(self, cookie):
        lottery_url = self.base_url + 'growth_api/v1/lottery/draw'
        res = requests.post(url=lottery_url, headers=self.headers, cookies={'Cookie': cookie}).content
        res = json.loads(res)
        return res


    def main(self):
        msg_all = ""
        i = 1
        for juejin_cookie in self.juejin_cookie_list:
            cookie = str(juejin_cookie.get("juejin_cookie"))
            sign_msg = self.sign(cookie=cookie)['err_msg']
            lottery_msg = self.lottery(cookie=cookie)['err_msg']
            msg = f"账号 {i}\n掘金签到结果\n" + sign_msg + "\n掘金抽奖结果\n" + lottery_msg
            i += 1
            msg_all += msg + '\n\n'
        return msg_all


if __name__ == '__main__':
    data = get_data()
    _juejin_cookie_list = data.get("JUEJIN_COOKIE_LIST", [])
    res = JuejinCheckIn(juejin_cookie_list=_juejin_cookie_list).main()
    print(res)
    send("掘金", res)