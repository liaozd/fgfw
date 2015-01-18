#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3
import webbrowser
import sys
import os
import re
import time

__version__ = '1.0'
__author__ = 'http://weibo.com/liaozd'

# api from:http://michaelliao.github.com/sinaweibopy/
from weibo import APIClient

from retry import *
from keyfile import *
try:
    import json
except ImportError:
    import simplejson as json

# setting sys encoding to utf-8
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

# token file path
save_access_token_file = 'access_token.txt'
file_path = os.getcwd() + os.path.sep
access_token_file_path = file_path + save_access_token_file

client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)


def make_access_token():
    authorize_url = client.get_authorize_url(REDIRECT_URL)
    print(authorize_url)
    webbrowser.open_new(authorize_url)
    code = raw_input('authencation code: ')

    request = client.request_access_token(code, REDIRECT_URL)
    access_token = request.access_token
    expires_in = request.expires_in
    print 'access token: ', access_token
    print 'expire: ', expires_in
    #得到token
    print request['access_token']
    save_access_token(request)


def save_access_token(request):
    '''将access token保存到本地'''
    f = open(access_token_file_path, 'w')
    f.write(request['access_token']+' ' + str(request['expires_in']))
    f.close()

@retry(1)
def apply_access_token():
    '''从本地读取及设置access token'''
    try:
        token = open(access_token_file_path, 'r').read().split()
        if len(token) != 2:
            make_access_token()
            return False
        # 过期验证
        access_token, expires_in = token
        try:
            client.set_access_token(access_token, expires_in)
        except StandardError, e:
            if hasattr(e, 'error'):
                if e.error == 'expired_token':
                    # token过期重新生成
                    make_access_token()
            else:
                pass
    except:
        make_access_token()
    return False


def expand_short_url(short_url):
    responsejson = client.get.short_url__expand(url_short='http://t.cn/RZNTSzw')
    return responsejson['urls'][0]['url_long']
    # not use api way
    # response = urllib2.urlopen(short_url)
    # return response.url


def get_resent_mentions(count=10):
    # return mentions in json format
    # weibo api doc
    # http://open.weibo.com/wiki/2/statuses/mentions
    mentions = client.get.statuses__mentions(count=count)
    return mentions


def filter_url(text):
    # from weibo text msg filter out the short url
    url = re.findall(r'http://t.cn/[\w+]{7,}', text)
    return url


def dump_mentions_to_database(mentions):
    database_file = 'my.db'
    file_path = os.getcwd() + os.path.sep
    database_file_path = file_path + database_file

    conn = sqlite3.connect(database_file_path)
    print "Opened database successfully"
    conn.execute('''CREATE TABLE IF NOT EXISTS LINKS
           (
           USERID INT NOT NULL,
           CREATED_AT datetime,
           MID INT NOT NULL,
           YOUTUBE_URL CHAR(120) PRIMARY KEY,
           DOWNLOADED BOOLEAN,
           YOUKU_URL CHAR(120),
           UPLOADED BOOLEAN
           );''')
    statuses = mentions['statuses']

    for oneMsg in statuses:
        print oneMsg['user']['id'], oneMsg['mid'], oneMsg['created_at']
        user_id = oneMsg['user']['id']
        mid = oneMsg['mid']
        craeted_at = oneMsg['created_at']
        short_url = filter_url(oneMsg['text'])
        if not short_url:
            continue
        youtube_url = expand_short_url(short_url[-1])
        print youtube_url
        try:
            conn.execute('INSERT INTO LINKS (USERID, MID, YOUTUBE_URL) VALUES ({0}, {1}, "{2}")'.format(user_id, mid, youtube_url))
            print youtube_url
        except sqlite3.IntegrityError:
            print 'Youtube link already exists: {}'.format(youtube_url)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    apply_access_token()
    # i = 1
    # while i < 10:
    #     print time.strftime("%Y-%m-%d %A %X %Z", time.localtime())
    mentions = get_resent_mentions(count=10)
    # for i in mentions['statuses']:
    #     print i['user']['id'], i['text']
    dump_mentions_to_database(mentions=mentions)
        # i += 1
        # time.sleep(600)


