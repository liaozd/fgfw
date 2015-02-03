#!/usr/bin/env python
import sqlite3
import time

__author__ = 'liao'

# api from https://github.com/Davidigest/pyYouku
# youku upload management page http://i.youku.com/u/videos

from keyfile import CLIENT_ID, ACCESS_TOKEN
from config import *

# my fork of youku
# https://github.com/hanguokai/youku
import sys
sys.path.append('/home/liao/git-repos/youku/youku/')
import imp
YoukuUpload = imp.load_source('YoukuUpload', '/home/liao/git-repos/youku/youku/youku_upload.py')


def uploader():
    my_name = "uploader"
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    print my_name.rjust(12, '+'), 'Checking Database for new file to push'
    sql = 'SELECT TITLE, CATEGORIES, FILEPATH, YOUTUBE_URL FROM LINKS WHERE UPLOADED==0 AND DOWNLOADED==1 ORDER BY CREATED_AT ASC LIMIT 1;'
    c.execute(sql)
    sql_result = c.fetchone()
    db.close()

    if sql_result:
        title, categories, filepath, youtubeURL = sql_result
        if ' & ' in categories:
            categories = categories.replace(' & ', ',')
        file_info = {
          'title': title,
          'tags': categories,
          'copyright_type': 'reproduced',
          'description': 'Automatically uploaded by @liaozd, original URL: {0}'.format(youtubeURL),
        }
        youku = YoukuUpload.YoukuUpload(CLIENT_ID, ACCESS_TOKEN, filepath)
        print my_name.rjust(12, "+"), 'uploading "{0}" to YOUKU ..........'.format(filepath)
        try:
            print youku.upload(file_info)
            print my_name.rjust(12, "+"), 'uploading {0} finished!!!!!!!'.format(title)
        except:
            '''
            requests.exceptions.ConnectionError: HTTPConnectionPool(host='119.167.145.45', port=80):
            Max retries exceeded with url: /gupload/upload_slice?upload_token=MzAwODk3MjNfMDEwMDY0M0FBMjU0Q0U0Mzg1RkJCODAwNjVEQ0MzQjAwRjRDQ0ItN0JDRS1EOEI0LTZBMDktOTJGNzA3NEZDQjQyXzFfYTkxM2M2Y2Q0Mjk2MTUxZWZkMWJhNzY0MWQ0YmZhMzk%3D&length=2097152&slice_task_id=37&hash=2782107e52bec2bd0a75dbc971b00c9a&offset=75497472
            (Caused by <class 'httplib.BadStatusLine'>: '')
            '''
            print my_name.rjust(12, "+"), 'uploading fail, sleep for a while, and try again.....'
            time.sleep(300)
            return False

        db = sqlite3.connect(DATABASE)
        c = db.cursor()
        sql, values = 'UPDATE LINKS SET UPLOADED=1 WHERE YOUTUBE_URL=?', (youtubeURL,)
        c.execute(sql, values)
        db.commit()
        db.close()
        return True


def cleaner():
    # TODO check for integrity from youku, then delete the mp4 file
    pass


def pusher(sleep_time=190):
    my_name = 'pusher'
    while True:
        print my_name.rjust(12, '+'), 'start at {0}'.format(time.strftime("%Y-%m-%d %A %X %Z", time.localtime()))
        if uploader():
            time.sleep(5)
        else:
            print my_name.rjust(12, '+'), 'takes a snap for {0}s'.format(sleep_time)
            time.sleep(sleep_time)

if __name__ == '__main__':
    pusher()