# -*- coding: utf-8 -*-
import requests

__version__ = '20210918-133'

def get_present_ver():
    ver_msg = f'checkinpanel 当前版本：{__version__}'
    return ver_msg

def get_latest_ver():
    url = "https://ghproxy.com/https://raw.githubusercontent.com/Oreomeow/checkinpanel/master/utils_ver.py"
    try:
        r = requests.get(url=url, timeout=3)
    except Exception as e:
        ver_msg = f'获取最新版本失败，错误信息如下：\n{e}'
    else:
        raw = r.text
        latest_ver = raw.split("\n\n")[1].split("'")[1]
        ver_msg = f'最新版本：{latest_ver}'
    return ver_msg

def print_ver():
    print(f'{get_present_ver()}，{get_latest_ver()}\n')