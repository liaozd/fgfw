#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
import sqlite3

__version__ = '1.0'
__author__ = 'http://weibo.com/liaozd'

# api from:http://michaelliao.github.com/sinaweibopy/
from weibo import APIClient
import webbrowser
import sys, os
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
save_access_token_file  = 'access_token.txt'
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
    re = (http://t.cn/[\w+]{7,})
    pass

def dump_mentions_to_database(mentions):
    database_file = 'my.db'
    file_path = os.getcwd() + os.path.sep
    database_file_path = file_path + database_file
    print database_file_path
    conn = sqlite3.connect(database_file_path)
    print "Opened database successfully"
    conn.execute('''CREATE TABLE IF NOT EXISTS LINKS
           (
           USERID INT NOT NULL,
           CREATED_AT datetime,
           MID INT NOT NULL,
           YOUTUBE_URL CHAR(60) PRIMARY KEY,
           YOUKU_UL CHAR(100)
           );''')
    statuses = mentions['statuses']
    for tweety in statuses:
        print tweety['user']['id'], tweety['mid'], tweety['created_at']
        print tweety['text']
        try:
            conn.execute("INSERT INTO LINKS (USERID, MID, YOUTUBE_URL) VALUES ({0}, {1}, {2})".format(tweety['user']['id'], tweety['mid'], tweety['text']))
        except sqlite3.IntegrityError:
            print 'ERROR: youtube link already exists: {}'.format(tweety['text'])
        # INSERT INTO LINKS (USERID, MID, YOUTUBE_URL) VALUES (5144344398, 3800000892661694, ' @liaozhuodi youtube link: http://t.cn/RZNTSzw testEnd')
    conn.commit()
    conn.close()

# https://github.com/Davidigest/pyYouku
# batch upload video to youku

if __name__ == "__main__":
    apply_access_token()
    mentions = get_resent_mentions(count=5)
    # for i in mentions['statuses']:
    #     print i['user']['id'], i['text']
    dump_mentions_to_database(mentions=mentions)


