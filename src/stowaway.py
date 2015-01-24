#!/usr/bin/env python

__author__ = 'liao'

# api from https://github.com/Davidigest/pyYouku
# youku upload management page http://i.youku.com/u/videos

from youku import YoukuUpload
from keyfile import CLIENT_ID, ACCESS_TOKEN


def upload():
    file_info = {
      'title': u'my test',
      'tags': 'upload test,IO,',
      'description': '1st upload test',
    }
    file = "/tmp/PAY WHAT YOU WANT for Django tutorials!-CQmBKYtLr5A.mp4"
    youku = YoukuUpload(CLIENT_ID, ACCESS_TOKEN, file)
    youku.upload(file_info)

upload()