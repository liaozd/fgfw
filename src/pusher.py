#!/usr/bin/env python
import sqlite3

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


def upload():

    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    print "Checking Database for new file to push"
    sql = 'SELECT FILEPATH, YOUTUBE_URL FROM LINKS WHERE UPLOADED==0 AND DOWNLOADED==1 ORDER BY CREATED_AT ASC LIMIT 1;'
    c.execute(sql)
    sql_result = c.fetchone()
    if sql_result:
        filepath, youtubeURL = sql_result
        basename = os.path.basename(filepath).split('.')[0]
        file_info = {
          'title': basename,
          'tags': 'youtube',
          'description': 'Automatically upload by weibo @liaozd, origin URL is: {0}'.format(youtubeURL),
        }
        youku = YoukuUpload.YoukuUpload(CLIENT_ID, ACCESS_TOKEN, filepath)
        print 'Uploading "{0}" to youku.com'.format(basename)
        print youku.upload(file_info)
        print "Uploading finished"
        sql = 'UPDATE LINKS SET UPLOADED=1 WHERE YOUTUBE_URL="{0}";'.format(youtubeURL)
        c.execute(sql)
        db.commit()
    db.close()

upload()