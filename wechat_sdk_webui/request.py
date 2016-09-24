# -*- coding:utf-8 -*-
"""微信通信协议封装
"""
import re
import requests
from urllib import quote

import utils


# 微信根据 cookie 对用户鉴权
_req = requests.Session()
# 缓存自己及好友的 username 等
_db = dict()


def get_uuid():
    url = 'https://login.wx.qq.com/jslogin'
    redirect_uri = 'https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxnewloginpage'
    payload = {
        'appid': 'wx782c26e4c19acffb',
        'redirect_uri': quote(redirect_uri, ''),
        'fun': 'new',
        'lang': 'en_US',
        '_': utils.get_timestamp(),
    }

    r = _req.get(url, params=payload)

    ptn = re.compile(r'window.QRLogin.code = (\d+); window.QRLogin.uuid = "([^"]+)";')

    m = ptn.search(r.text)
    if m:
        code, uuid = m.groups()
        if code != '200':
            print 'Unexpect Response Code in get_uuid: %s' % code
        else:
            return uuid
    return None


def login():
    uuid = get_uuid()

    print uuid

    if not uuid:
        return


def main():
    login()


if __name__ == '__main__':
    main()