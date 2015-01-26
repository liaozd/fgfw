#!/usr/bin/env python
import sqlite3

__author__ = 'liao'

# api from https://github.com/Davidigest/pyYouku
# youku upload management page http://i.youku.com/u/videos

from youku import YoukuUpload
from keyfile import CLIENT_ID, ACCESS_TOKEN
from config import *


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
        print 'Uploading "{0}" to youku.com'.format(basename)
        youku = YoukuUpload(CLIENT_ID, ACCESS_TOKEN, filepath)
        youku.upload(file_info)
        print "Uploading finished"
        sql = 'UPDATE LINKS SET UPLOADED=1 WHERE YOUTUBE_URL="{0}";'.format(youtubeURL)
        c.execute(sql)
        db.commit()
    db.close()
upload()