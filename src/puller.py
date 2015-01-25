import sqlite3
import youtube_dl
from config import DATABASE


def download(youtubeURL, destination=""):
    ydl = youtube_dl.YoutubeDL({'outtmpl': 'download/%(title)s.%(ext)s'})
    with ydl:
        result = ydl.extract_info(
            youtubeURL,
            # download=False, # if you just want to extract the info
        )

    if 'entries' in result:
        # A playlist or a list of videos
        video = result['entries'][0]
    else:
        # Just one video
        video = result
    print(video)


def puller():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    print "Checking Database for new youtube entry"
    c.execute('SELECT CREATED_AT, YOUTUBE_URL, DOWNLOADED FROM LINKS WHERE DOWNLOADED==0;')
    print c.fetchone()
    print c.fetchone()
    conn.close()


if __name__ == "__main__":
    puller()
    youtubeURL = 'http://www.youtube.com/watch?v=BaW_jenozKc'
    download(youtubeURL)

