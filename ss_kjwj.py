# -*- coding: utf8 -*-

import os, requests, time
from utils import get_data
from notify_mtr import send


class KJWJCheckIn:
    def __init__(self, kjwj_account_list):
        self.kjwj_account_list = kjwj_account_list


    def login(self, usr, pwd):
        login_url = 'https://www.kejiwanjia.com/wp-json/jwt-auth/v1/token'
        headers = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; PBEM00) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.52 Mobile Safari/537.36'
        }
        data = {
            'nickname': '',
            'username': usr,
            'password': pwd,
            'code': '',
            'img_code': '',
            'invitation_code': '',
            'token': '',
            'smsToken': '',
            'luoToken': '',
            'confirmPassword': '',
            'loginType': ''
        }
        res = requests.post(login_url, headers=headers, data=data)
        if res.status_code == 200:
            status = res.json()
            login_stat = f"账号：{status.get('name')} 登陆成功"
            id = f"ID：{status.get('id')}"
            coin = f"金币：{status.get('credit')}"
            level = f"等级：{status.get('lv').get('lv').get('name')}"
            token = status.get('token')
            check_url = 'https://www.kejiwanjia.com/wp-json/b2/v1/userMission'
            check_head = {
                'authorization': f'Bearer {token}',
                'origin': 'https://www.kejiwanjia.com',
                'referer': 'https://www.kejiwanjia.com/task',
                'user-agent': 'Mozilla/5.0 (Linux; Android 10; PBEM00) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.52 Mobile Safari/537.36'
            }
            resp = requests.post(check_url, headers=check_head)
            if resp.status_code == 200:
                info = resp.json()
                # print(info)
                if 'date' in info:
                    sign_info = f"签到成功：{info.get('credit')} 金币"
                else:
                    sign_info = f"已经签到：{info}金币"
        else:
            sign_info = '账号登陆失败: 账号或密码错误'
        return login_stat, id, coin, level, sign_info


    def main(self):
        msg_all = ""
        i = 1
        for kjwj_account in self.kjwj_account_list:
            username = str(kjwj_account.get("kjwj_username"))
            password = str(kjwj_account.get("kjwj_password"))
            login_stat, id, coin, level, sign_info = self.login(usr=username, pwd=password)
            msg = (
                f"===> 账号{i} 开始 <===" 
                f"\n{login_stat}"
                f"\n{id}"
                f"\n{coin}"
                f"\n{level}"
                "\n===> 签到信息 <===\n"
                f"{sign_info}"
            )
            i += 1
            msg_all += msg + '\n\n'
        return msg_all


if __name__ == '__main__':
    data = get_data()
    _kjwj_account_list = data.get("KJWJ_ACCOUNT_LIST", [])
    res = KJWJCheckIn(kjwj_account_list=_kjwj_account_list).main()
    print(res)
    send("科技玩家", res)