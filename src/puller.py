
import sqlite3

import youtube_dl
from config import DATABASE


def puller(youtubeURL):
    ydl = youtube_dl.YoutubeDL({'outtmpl': '%(title)s.%(ext)s'})
    with ydl:
        result = ydl.extract_info(
            youtubeURL,
            download=False, # if you just want to extract the info
        )

    if 'entries' in result:
        # A playlist or a list of videos
        video = result['entries'][0]
    else:
        # Just one video
        video = result
    print(video)
    video_url = video['url']
    print(video_url)


if __name__ == "__main__":
    conn = sqlite3.connect(DATABASE)
    print "Check Database for new youtube entry"

    youtubeURL = 'http://www.youtube.com/watch?v=BaW_jenozKc'
    puller(youtubeURL)

