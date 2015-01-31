#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3
import webbrowser
import sys
import re
import dateutil.parser

from config import *

__version__ = '1.0'
__author__ = 'http://weibo.com/liaozd'

# the api is from:http://michaelliao.github.com/sinaweibopy/
from helper.weibo import APIClient
from helper.retry import *
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


class WeiboListener(object):

    def __init__(self):
        # token file path
        save_access_token_file = 'access_token.txt'
        file_path = os.getcwd() + os.path.sep
        self.access_token_file_path = file_path + save_access_token_file
        self.client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)

        # build database if not there
        db = sqlite3.connect(DATABASE)
        print "Connect to database successfully"
        cursor = db.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS LINKS
                    (
                    USERID INT NOT NULL,
                    CREATED_AT datetime,
                    MID INT NOT NULL,
                    YOUTUBE_URL CHAR(120) PRIMARY KEY,
                    TITLE CHAR(200),
                    DOWNLOADED BOOLEAN NOT NULL DEFAULT 0,
                    CATEGORIES CHAR(100),
                    DESCRIPTION CHAR(300),
                    FILEPATH CHAR(220),
                    YOUKU_URL CHAR(120),
                    UPLOADED BOOLEAN NOT NULL DEFAULT 0
                    )''')
        db.commit()
        db.close()

    def make_access_token(self):
        authorize_url = self.client.get_authorize_url(REDIRECT_URL)
        print(authorize_url)
        webbrowser.open_new(authorize_url)
        code = raw_input('authencation code: ')

        request = self.client.request_access_token(code, REDIRECT_URL)
        access_token = request.access_token
        expires_in = request.expires_in
        print 'access token: ', access_token
        print 'expire: ', expires_in
        #得到token
        print request['access_token']
        self.save_access_token(request)

    def save_access_token(self, request):
        '''将access token保存到本地'''
        f = open(self.access_token_file_path, 'w')
        f.write(request['access_token']+' ' + str(request['expires_in']))
        f.close()

    @retry(1)
    def apply_access_token(self):
        '''从本地读取及设置access token'''
        try:
            token = open(self.access_token_file_path, 'r').read().split()
            if len(token) != 2:
                self.make_access_token()
                return False
            # 过期验证
            access_token, expires_in = token
            try:
                self.client.set_access_token(access_token, expires_in)
            except StandardError, e:
                if hasattr(e, 'error'):
                    if e.error == 'expired_token':
                        # token过期重新生成
                        print "Weibo token expired, need re generate again!"
                        self.make_access_token()
                else:
                    pass
        except:
            self.make_access_token()
        return False

    def filter_url(self, text):
        # from weibo text msg, take out the short url in the last
        url = re.findall(r'http://t.cn/[\w+]{7,}', text)
        if url:
            return url[-1]
        else:
            return None

    def expand_short_url(self, short_url):
        responsejson = self.client.get.short_url__expand(url_short=short_url)
        return responsejson['urls'][0]['url_long']
        # Another way to get full url
        # response = urllib2.urlopen(short_url)
        # return response.url

    def youtube_url_sentry(self, short_url):
        # sample url
        # single video: https://www.youtube.com/watch?v=pA5MFlY5Klc
        # playlist: https://www.youtube.com/watch?v=mdcA5fR91S8&list=PLOU2XLYxmsII_38oWcnQzXs9K9HKBMg-e
        #           https://www.youtube.com/watch?v=IXvpvvb67hw&list=PLA64AFAE28B8DD0FD
        # long_url = "https://www.youtube.com/watch?v=IXvpvvb67hw&list=PLA64AFAE28B8DD0FD"
        if short_url is None:
            return None
        long_url = self.expand_short_url(short_url)
        single_url = re.findall(r'^https://www.youtube.com/watch\?v=[\w_%+-]{11}$', long_url)
        playlist_url = re.findall(r'^https://www.youtube.com/watch\?v=[\w+]{11}&list=$[\w_%+-]{18,}$', long_url)
        if single_url:
            return single_url[0]
        elif playlist_url:
            return playlist_url
        else:
            return None


    def reply_to_mentioner(self):pass
        # TODO send weibo mentioner a msg

    def get_resent_mentions(self, count=15):
        # return mentions in json format
        # weibo api doc
        # http://open.weibo.com/wiki/2/statuses/mentions
        mentions = self.client.get.statuses__mentions(count=count)
        return mentions

    def dump_mentions_to_database(self, mentions):
        db = sqlite3.connect(DATABASE)
        cursor = db.cursor()
        statuses = mentions['statuses']
        for oneMsg in statuses:
            # print oneMsg['user']['id'], oneMsg['mid'], oneMsg['created_at'], oneMsg['text']
            user_id = oneMsg['user']['id']
            mid = oneMsg['mid']
            created_at = oneMsg['created_at']
            created_at = dateutil.parser.parse(created_at)
            created_at = created_at.strftime("%Y-%m-%d %H:%M:%S")
            short_url = self.filter_url(oneMsg['text'])
            youtube_url = self.youtube_url_sentry(short_url)
            if youtube_url:
                print youtube_url
                self.reply_to_mentioner()
            else:
                continue
            try:
                sql = 'INSERT INTO LINKS (USERID, CREATED_AT, MID, YOUTUBE_URL) VALUES ({0},"{1}",{2},"{3}");'.format(
                    user_id,
                    created_at,
                    mid,
                    youtube_url)
                cursor.execute(sql)
                print "Update DB - INSERT: ", youtube_url,
            except sqlite3.IntegrityError:
                # print 'Youtube link already exists: {}'.format(youtube_url)
                continue
        db.commit()
        db.close()

weiboer = WeiboListener()
weiboer.apply_access_token()


def listener(count=10, sleeptime=280):
    """listen to my weibo and push new mention to db
    """
    while True:
        mentions = weiboer.get_resent_mentions(count=count)
        print "{0} listener - last weibo mention is {1}".format(time.strftime("%Y-%m-%d %A %X %Z", time.localtime()), mentions['statuses'][0]['created_at'])
        weiboer.dump_mentions_to_database(mentions=mentions)
        time.sleep(sleeptime)

if __name__ == "__main__":
    listener()

