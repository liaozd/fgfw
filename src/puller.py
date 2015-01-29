import os
import sqlite3
import time
import youtube_dl
from config import DATABASE
from helper.slugify import slugify


def myYoutubeDL(youtubeURL, destination="download/"):
    print "Get video info"
    # prepare filename and path to save the file
    ydl = youtube_dl.YoutubeDL()
    r = ydl.extract_info(youtubeURL, download=False)
    basename = '.'.join((slugify(r['title']), r['ext']))
    filepath = os.path.join(destination, basename)
    # print "Start to download {}".format(filepath)
    ydl = youtube_dl.YoutubeDL({'outtmpl': filepath})
    r = ydl.extract_info(youtubeURL, download=True)
    r['filepath'] = filepath
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
    downloadFlag = False
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    print "downloader Checking Database for new youtube entry"
    # SELECT the oldest youtube link have not been downloaded
    sql = 'SELECT YOUTUBE_URL FROM LINKS WHERE DOWNLOADED==0 ORDER BY CREATED_AT ASC LIMIT 1;'
    c.execute(sql)
    youtubeURL = c.fetchone()
    if youtubeURL:
        youtubeURL = youtubeURL[0]
        # Start download and return the path name
        r = myYoutubeDL(youtubeURL)
        print r['filepath']
        print r['categories']
        print r['description']
        print youtubeURL
        sql = 'UPDATE LINKS SET TITLE="{0}",FILEPATH="{1}", DOWNLOADED=1, CATEGORIES="{2}" WHERE YOUTUBE_URL="{3}";'.format(
            r['title'],
            r['filepath'],
            r['categories'],
            youtubeURL)
        c.execute(sql)
        print "Download finished!"
        print "UPDATE DATABASE WITH FILE PATH: ", r['filepath']
        downloadFlag = True
    db.commit()
    db.close()
    return downloadFlag


def puller(sleeptime=190):
    while True:
        print "{0} puller start".format(time.strftime("%Y-%m-%d %A %X %Z", time.localtime()))
        downloader()
        print "puller takes a snap for {0}s".format(sleeptime)
        time.sleep(sleeptime)

if __name__ == "__main__":
    puller()

