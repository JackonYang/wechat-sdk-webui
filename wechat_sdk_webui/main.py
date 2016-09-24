# -*- coding:utf-8 -*-
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


def waiting4login(uuid):
    """step2 of login"""
    while True:
        print 'waiting...'
        redirect_uri = request.is_logined(uuid)
        if redirect_uri:
            return redirect_uri


def main():
    uuid = show_qrcode()

    waiting4login(uuid)

    # kill image window


if __name__ == '__main__':
    main()
