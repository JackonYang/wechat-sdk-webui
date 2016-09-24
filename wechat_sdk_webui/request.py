# -*- coding:utf-8 -*-
"""微信通信协议封装
"""
import json
import re
import requests
from urllib import quote
from xml.dom import minidom

import utils


# 微信根据 cookie 对用户鉴权
_req = requests.Session()
_db = {
    'uuid': None,
    'pass_ticket': None,
    'base_request': None,
    'username': None,
    'uin': None,
    'sid': None,
    'skey': None,
    'sync_key': None,
}


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
            _db['uuid'] = uuid
            return uuid
    return None


def get_qrcode(uuid):
    url = 'https://login.weixin.qq.com/qrcode/%s' % uuid
    r = _req.get(url)
    return r.content


def is_logined(uuid):
    """detect whether user has logined

    return redirect_uri
    """
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

    _db['base_request'] = {
        'Uin': params['wxuin'],
        'Sid': params['wxsid'],
        'Skey': params['skey'],
        'DeviceID': utils.gen_device_id(),
    }
    _db['pass_ticket'] = params.get('pass_ticket')
    _db['uin'] = params.get('wxuin')
    _db['sid'] = params.get('wxsid')
    _db['skey'] = params.get('skey')


def wx_init():
    pass_ticket, base_request = _db['pass_ticket'], _db['base_request']
    url = 'https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxinit?r=%s&lang=en_US&pass_ticket=%s' % (utils.get_timestamp(), pass_ticket)
    data = {'BaseRequest': base_request}
    r = _req.post(url, data=json.dumps(data))
    r.encoding = 'utf-8'
    data = r.json()

    _db['username'] = data.get('User', dict()).get('UserName')
    _db['skey'] = data.get('SKey')
    _db['sync_key'] = data.get('SyncKey')

    for key, value in _db.items():
        print key, value
    return data


def status_notify():
    pass_ticket, base_request = _db['pass_ticket'], _db['base_request']

    timestamp = utils.get_timestamp()
    url = 'https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxstatusnotify?r=%s&lang=en_US&pass_ticket=%s' % (timestamp, pass_ticket)
    data = json.dumps({
        'BaseRequest': base_request,
        "Code": 3,
        "FromUserName": _db['username'],
        "ToUserName": _db['username'],
        "ClientMsgId": timestamp,
    })
    r = _req.post(url, data=data)
    r.encoding = 'utf-8'
    data = r.json()

    return data


def get_contactlist():
    url = 'https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxgetcontact?lang=en_US&r=%s&seq=0&skey=%s' % (utils.get_timestamp(), _db['skey'])

    r = _req.post(url)
    r.encoding = 'utf-8'
    return r.json()
