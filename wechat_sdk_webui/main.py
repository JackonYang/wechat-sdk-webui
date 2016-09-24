# -*- coding:utf-8 -*-
import codecs
import json
import StringIO
from PIL import Image

import request


def show_qrcode():
    """step1 of login"""
    uuid = request.get_uuid()
    img_src = request.get_qrcode(uuid)

    msg = 'Scan QR Code to log in'
    image = Image.open(StringIO.StringIO(img_src))
    image.show(title=msg)
    image.close()

    print '!!! %s' % msg
    return uuid


def login(uuid):
    """step2 of login"""
    redirect_uri = None
    while True:
        print 'waiting...'
        redirect_uri = request.is_logined(uuid)
        if redirect_uri:
            break

    base_request = request.did_login(redirect_uri)
    return base_request


def load_initial_data():
    data = request.wx_init()
    request.status_notify()

    with codecs.open('init_data.json', 'w', 'utf8') as f:
        f.write(json.dumps(data))


def main():
    uuid = show_qrcode()

    login(uuid)

    # kill image window

    load_initial_data()

    data = request.get_contactlist()

    with codecs.open('contact_list.json', 'w', 'utf8') as f:
        f.write(json.dumps(data))


if __name__ == '__main__':
    main()
