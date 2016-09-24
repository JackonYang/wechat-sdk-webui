# -*- coding:utf-8 -*-
"""微信通信协议封装
"""
import re
import requests
from urllib import quote
from xml.dom import minidom

import utils


# 微信根据 cookie 对用户鉴权
_req = requests.Session()


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


def get_qrcode(uuid):
    url = 'https://login.weixin.qq.com/qrcode/%s' % uuid
    r = _req.get(url)
    return r.content


def is_logined(uuid):
    """detect whether user has logined"""
    url = 'https://login.wx.qq.com/cgi-bin/mmwebwx-bin/login'
    payload = {
        'uuid': uuid,
        'tip': 0,
        '_': utils.get_timestamp(),
    }
    r = _req.get(url, params=payload)

    ptn = re.compile(r'window.redirect_uri="([^"]+)";')

    m = ptn.search(r.text)
    return m and m.group(1)


def did_login(redirect_uri):
    url = redirect_uri + '&fun=new&version=v2'
    r = _req.get(url)
    r.encoding = 200
    dom = minidom.parseString(r.text)
    root = dom.documentElement

    params = {n.nodeName: n.firstChild and n.firstChild.nodeValue
              for n in root.childNodes}
    base_request = {
        'Uin': params['wxuin'],
        'Sid': params['wxsid'],
        'Skey': params['skey'],
        'DeviceID': utils.gen_device_id(),
    }
    return params.get('pass_ticket'), base_request
