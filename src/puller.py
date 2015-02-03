import os
import sqlite3
import time
import youtube_dl
from config import DATABASE
from helper.slugify import slugify


def my_utub_dl(youtube_url, destination="download/"):
    my_name = 'my_utub_dl'
    print my_name.rjust(12, '+'), 'is getting video info'
    # prepare filename and path to save the file
    ydl = youtube_dl.YoutubeDL()
    r = ydl.extract_info(youtube_url, download=False)
    basename = '.'.join((slugify(r['title']), r['ext']))
    file_path = os.path.join(destination, basename)
    # print "Start to download {}".format(file_path)
    ydl = youtube_dl.YoutubeDL({'outtmpl': file_path})
    r = ydl.extract_info(youtube_url, download=True)
    r['file_path'] = file_path
    # for key in r:
    #     print key, ":", r[key]
    # if you just want to extract the info
    # >>> import youtube_dl as yt
    # >>> help(yt)
    # http://willdrevo.com/downloading-youtube-and-soundcloud-audio-with-python-and-pandas/

    # ydl.extract_info()
    # if 'entries' in result:
    #     # A playlist or a list of videos
    #     video = result['entries'][0]
    # else:
    #     # Just one video
    #     video = result
    # print(video)
    return r


def downloader():
    my_name = 'downloader'
    download_flag = False
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    print my_name.rjust(12, '+'), 'Checking Database for new youtube entry.'
    # SELECT the oldest youtube link have not been downloaded
    sql = 'SELECT YOUTUBE_URL FROM LINKS WHERE DOWNLOADED==0 ORDER BY CREATED_AT ASC LIMIT 1;'
    c.execute(sql)
    youtube_url = c.fetchone()
    if youtube_url:
        youtube_url = youtube_url[0]
        # Start download and return the path name
        r = my_utub_dl(youtube_url)
        # categories is a single element list, and it is a equivalence to youku tag
        if r['categories']:
            categories = r['categories'][0]
        # title = r['title'].replace('"', '\\"').replace("'", "\\'")
        sql, value = 'UPDATE LINKS SET TITLE=?, FILEPATH=?, DOWNLOADED=1, CATEGORIES=? WHERE YOUTUBE_URL=?',\
                     (r['title'], r['file_path'], categories, youtube_url)
        c.execute(sql, value)
        print my_name.rjust(12, '+'), 'download finished!'
        print my_name.rjust(12, '+'), 'UPDATE DATABASE WITH FILE PATH: ', r['file_path']
        download_flag = True
    db.commit()
    db.close()
    return download_flag


def puller(sleep=190):
    my_name = 'puller'
    while True:
        print my_name.rjust(12, '+'), 'start at {0}'.format(time.strftime('%Y-%m-%d %A %X %Z', time.localtime()))
        downloader()
        print my_name.rjust(12, '+'), 'takes a snap for {0}s'.format(sleep)
        time.sleep(sleep)

if __name__ == "__main__":
    puller()

