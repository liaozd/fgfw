#!/usr/bin/env python
import sqlite3
import time

__author__ = 'liao'

# api from https://github.com/Davidigest/pyYouku
# youku upload management page http://i.youku.com/u/videos


from keyfile import CLIENT_ID, ACCESS_TOKEN
from config import *
# import youku # pip install youku

# my fork youku
import sys
sys.path.append('/home/liao/git-repos/youku/youku/')
import imp
YoukuUpload = imp.load_source('YoukuUpload', '/home/liao/git-repos/youku/youku/youku_upload.py')


def uploader():

    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    print "Checking Database for new file to push"
    sql = 'SELECT TITLE, CATEGORIES, FILEPATH, YOUTUBE_URL FROM LINKS WHERE UPLOADED==0 AND DOWNLOADED==1 ORDER BY CREATED_AT ASC LIMIT 1;'
    c.execute(sql)
    sql_result = c.fetchone()
    if sql_result:
        title, categories, filepath, youtubeURL = sql_result
        print categories
        file_info = {
          'title': title,
          'tags': 'YouTube',
          'description': 'Automatically uploaded by @liao_zd, original URL: {0}'.format(youtubeURL),
        }
        youku = YoukuUpload.YoukuUpload(CLIENT_ID, ACCESS_TOKEN, filepath)
        print 'Uploading "{0}" to youku.com'.format(filepath)
        print youku.upload(file_info)
        print "Uploading finished"
        sql = 'UPDATE LINKS SET UPLOADED=1 WHERE YOUTUBE_URL="{0}";'.format(youtubeURL)
        c.execute(sql)
        db.commit()
    db.close()


def pusher(sleeptime=190):
    while True:
        print "{0} pusher start".format(time.strftime("%Y-%m-%d %A %X %Z", time.localtime()))
        uploader()
        print "pusher takes a snap for {0}s".format(sleeptime)
        time.sleep(sleeptime)

if __name__ == '__main__':
    pusher()