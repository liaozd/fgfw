import sqlite3
import youtube_dl
from config import DATABASE

def downloadTo(youtubeURL, destination="download/"):
    ydl = youtube_dl.YoutubeDL({'outtmpl': '{}%(title)s.%(ext)s'.format(destination)})
    result = ydl.extract_info(youtubeURL, download=True)
    # if you just want to extract the info
    # >>> import youtube_dl as yt
    # >>> help(yt)
    # http://willdrevo.com/downloading-youtube-and-soundcloud-audio-with-python-and-pandas/
    video_filepath = "{0}{1}.{2}".format(destination, result['title'], result['ext'])
    # ydl.extract_info()
    # if 'entries' in result:
    #     # A playlist or a list of videos
    #     video = result['entries'][0]
    # else:
    #     # Just one video
    #     video = result
    # print(video)
    return video_filepath

def puller():
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    print "Checking Database for new youtube entry"
    # SELECT the oldest youtube link have not been downloaded
    sql = 'SELECT  YOUTUBE_URL, CREATED_AT, DOWNLOADED FROM LINKS WHERE DOWNLOADED==0 ORDER BY CREATED_AT ASC LIMIT 1;'
    c.execute(sql)
    youtubeURL = c.fetchone()
    print youtubeURL
    if youtubeURL:
        youtubeURL = youtubeURL[0]
        # Start download and return the path name
        video_filepath = downloadTo(youtubeURL)
        sql = 'UPDATE LINKS SET FILEPATH="{0}", DOWNLOADED=1 WHERE YOUTUBE_URL="{1}";'.format(video_filepath, youtubeURL)
        c.execute(sql)
        print "Download finished!"
        print "UPDATE DATABASE WITH FILE PATH: ", video_filepath
    db.commit()
    db.close()

if __name__ == "__main__":
    puller()

