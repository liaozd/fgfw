import os
import sqlite3
import youtube_dl
from config import DATABASE
from helper.slugify import slugify


def downloadTo(youtubeURL, destination="download/"):
    print "Get video info"
    # prepare filename and path to save the file
    ydl = youtube_dl.YoutubeDL()
    r = ydl.extract_info(youtubeURL, download=False)
    basename = '.'.join((slugify(r['title']), r['ext']))
    video_filepath = os.path.join(destination, basename)
    print "Start to download {}".format(video_filepath)
    ydl = youtube_dl.YoutubeDL({'outtmpl': video_filepath})
    r = ydl.extract_info(youtubeURL, download=True)
    for key in r:
        print key, ":", r[key]

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
    return video_filepath


def puller():
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    print "Checking Database for new youtube entry"
    # SELECT the oldest youtube link have not been downloaded
    sql = 'SELECT  YOUTUBE_URL FROM LINKS WHERE DOWNLOADED==0 ORDER BY CREATED_AT ASC LIMIT 1;'
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

    sample = {u'upload_date': '20150106', u'extractor': u'youtube', u'height': 360, u'like_count': 20, u'duration': 100, u'player_url': None, u'id': u'ZGXD5wbixbE', u'view_count': 1590, u'playlist': None, u'title': u'How to Make Saltfish Cakes: Part 2 - Rhodes Across The Caribbean - BBC Food', u'playlist_index': None, u'dislike_count': 2, u'width': 640, u'categories': [u'Howto & Style'], u'age_limit': 0, u'annotations': None, u'webpage_url_basename': u'watch', u'display_id': u'ZGXD5wbixbE', u'description': u'Gary finishes off his saltfish cakes by deep-frying them.\n\nSubscribe here http://www.youtube.com/subscription_center?add_user=bbcfood\n\nMore delicious dishes at the Food YouTube channel: http://www.youtube.com/bbcfood\n\nThe new home of BBC Good Food http://www.bbcgoodfood.com/\n\nThis is a channel from BBC Worldwide who help fund new BBC programmes.', u'format': u'18 - 640x360', u'uploader': u'BBCFood', u'format_id': u'18', u'uploader_id': u'BBCFood', u'subtitles': None, u'url': u'https://r3---sn-nu5gi0c-npos.googlevideo.com/videoplayback?ms=au&mv=m&sparams=dur%2Cid%2Cinitcwndbps%2Cip%2Cipbits%2Citag%2Cmime%2Cmm%2Cms%2Cmv%2Cpl%2Cratebypass%2Crequiressl%2Csource%2Cupn%2Cexpire&mt=1422366034&requiressl=yes&ip=58.182.53.141&pl=21&id=o-ALuhu_QbWSF_PEtGHmJNJKjWFhpGN9WSshIYzOL2iy8c&fexp=900718%2C904848%2C907263%2C913441%2C927622%2C930676%2C936122%2C9406282%2C941004%2C942618%2C943917%2C947225%2C948124%2C949427%2C952302%2C952605%2C952901%2C955301%2C957103%2C957105%2C957201%2C959701&mm=31&expire=1422387730&ratebypass=yes&sver=3&dur=99.288&ipbits=0&key=yt5&mime=video%2Fmp4&signature=A52E7B908AAEFEC7EB23299B38D6DA995A711FA0.4BBB59E2B7614E646BD570A6CD7FCA79478CAC32&itag=18&source=youtube&upn=_H6K7YDb4ms&initcwndbps=1371250', u'extractor_key': 'Youtube', u'thumbnail': u'https://i.ytimg.com/vi/ZGXD5wbixbE/hqdefault.jpg', u'ext': u'mp4', u'webpage_url': u'https://www.youtube.com/watch?v=ZGXD5wbixbE', u'formats': [{u'format': u'nondash-171 - audio only (DASH audio)', u'url': u'https://r3---sn-nu5gi0c-npos.googlevideo.com/videoplayback?ms=au&lmt=1420637006451010&mv=m&sparams=clen%2Cdur%2Cgir%2Cid%2Cinitcwndbps%2Cip%2Cipbits%2Citag%2Ckeepalive%2Clmt%2Cmime%2Cmm%2Cms%2Cmv%2Cpl%2Crequiressl%2Csource%2Cupn%2Cexpire&mt=1422366034&requiressl=yes&ip=58.182.53.141&pl=21&id=o-ALuhu_QbWSF_PEtGHmJNJKjWFhpGN9WSshIYzOL2iy8c&fexp=900718%2C904848%2C907263%2C913441%2C927622%2C930676%2C936122%2C9406282%2C941004%2C942618%2C943917%2C947225%2C948124%2C949427%2C952302%2C952605%2C952901%2C955301%2C957103%2C957105%2C957201%2C959701&mm=31&expire=1422387730&sver=3&dur=99.241&ipbits=0&key=yt5&gir=yes&mime=audio%2Fwebm&signature=64E5BDF328E3E9739B4B5B8429E405368DD5A40C.1BD77E21076FEB6FC080B2CE29DEF23BF16238DA&clen=885873&itag=171&source=youtube&upn=_H6K7YDb4ms&initcwndbps=1371250&keepalive=yes&ratebypass=yes', u'vcodec': u'none', u'format_note': u'DASH audio', u'abr': 128, u'player_url': None, u'ext': u'webm', u'preference': -10050, u'format_id': u'nondash-171'}, {u'container': u'm4a_dash', u'format': u'nondash-140 - audio only (DASH audio)', u'url': u'https://r3---sn-nu5gi0c-npos.googlevideo.com/videoplayback?ms=au&lmt=1421241656406916&mv=m&sparams=clen%2Cdur%2Cgir%2Cid%2Cinitcwndbps%2Cip%2Cipbits%2Citag%2Ckeepalive%2Clmt%2Cmime%2Cmm%2Cms%2Cmv%2Cpl%2Crequiressl%2Csource%2Cupn%2Cexpire&mt=1422366034&requiressl=yes&ip=58.182.53.141&pl=21&id=o-ALuhu_QbWSF_PEtGHmJNJKjWFhpGN9WSshIYzOL2iy8c&fexp=900718%2C904848%2C907263%2C913441%2C927622%2C930676%2C936122%2C9406282%2C941004%2C942618%2C943917%2C947225%2C948124%2C949427%2C952302%2C952605%2C952901%2C955301%2C957103%2C957105%2C957201%2C959701&mm=31&expire=1422387730&sver=3&dur=99.287&ipbits=0&key=yt5&gir=yes&mime=audio%2Fmp4&signature=B8AEAC923ED2A6F05D9ED4BC13143335307B016B.1AC0D09F4C10E0F41176304C3080B06A4977CE0E&clen=1594596&itag=140&source=youtube&upn=_H6K7YDb4ms&initcwndbps=1371250&keepalive=yes&ratebypass=yes', u'vcodec': u'none', u'format_note': u'DASH audio', u'abr': 128, u'player_url': None, u'ext': u'm4a', u'preference': -10050, u'format_id': u'nondash-140', u'acodec': u'aac'}, {u'format': u'nondash-160 - 144p (DASH video)', u'url': u'https://r3---sn-nu5gi0c-npos.googlevideo.com/videoplayback?ms=au&lmt=1421241656835610&mv=m&sparams=clen%2Cdur%2Cgir%2Cid%2Cinitcwndbps%2Cip%2Cipbits%2Citag%2Ckeepalive%2Clmt%2Cmime%2Cmm%2Cms%2Cmv%2Cpl%2Crequiressl%2Csource%2Cupn%2Cexpire&mt=1422366034&requiressl=yes&ip=58.182.53.141&pl=21&id=o-ALuhu_QbWSF_PEtGHmJNJKjWFhpGN9WSshIYzOL2iy8c&fexp=900718%2C904848%2C907263%2C913441%2C927622%2C930676%2C936122%2C9406282%2C941004%2C942618%2C943917%2C947225%2C948124%2C949427%2C952302%2C952605%2C952901%2C955301%2C957103%2C957105%2C957201%2C959701&mm=31&expire=1422387730&sver=3&dur=99.280&ipbits=0&key=yt5&gir=yes&mime=video%2Fmp4&signature=FA415ECC27C36641E717A0AA6A622ED435DAE211.F6DA68D81A7E15D8F441AC68A750662D9E47FDB0&clen=1376770&itag=160&source=youtube&upn=_H6K7YDb4ms&initcwndbps=1371250&keepalive=yes&ratebypass=yes', u'format_note': u'DASH video', u'player_url': None, u'ext': u'mp4', u'preference': -10040, u'format_id': u'nondash-160', u'height': 144, u'acodec': u'none'}, {u'format': u'nondash-242 - 240p (DASH video)', u'url': u'https://r3---sn-nu5gi0c-npos.googlevideo.com/videoplayback?ms=au&lmt=1420637040489362&mv=m&sparams=clen%2Cdur%2Cgir%2Cid%2Cinitcwndbps%2Cip%2Cipbits%2Citag%2Ckeepalive%2Clmt%2Cmime%2Cmm%2Cms%2Cmv%2Cpl%2Crequiressl%2Csource%2Cupn%2Cexpire&mt=1422366034&requiressl=yes&ip=58.182.53.141&pl=21&id=o-ALuhu_QbWSF_PEtGHmJNJKjWFhpGN9WSshIYzOL2iy8c&fexp=900718%2C904848%2C907263%2C913441%2C927622%2C930676%2C936122%2C9406282%2C941004%2C942618%2C943917%2C947225%2C948124%2C949427%2C952302%2C952605%2C952901%2C955301%2C957103%2C957105%2C957201%2C959701&mm=31&expire=1422387730&sver=3&dur=99.200&ipbits=0&key=yt5&gir=yes&mime=video%2Fwebm&signature=BB5D3AA12FDD6187C03078E6DCE3861D2ADFE46D.482F0AF33CB85D927631DA6698EF1144EA6DED86&clen=2563832&itag=242&source=youtube&upn=_H6K7YDb4ms&initcwndbps=1371250&keepalive=yes&ratebypass=yes', u'format_note': u'DASH video', u'player_url': None, u'ext': u'webm', u'preference': -10040, u'format_id': u'nondash-242', u'height': 240, u'acodec': u'none'}, {u'format': u'nondash-133 - 240p (DASH video)', u'url': u'https://r3---sn-nu5gi0c-npos.googlevideo.com/videoplayback?ms=au&lmt=1421241659705814&mv=m&sparams=clen%2Cdur%2Cgir%2Cid%2Cinitcwndbps%2Cip%2Cipbits%2Citag%2Ckeepalive%2Clmt%2Cmime%2Cmm%2Cms%2Cmv%2Cpl%2Crequiressl%2Csource%2Cupn%2Cexpire&mt=1422366034&requiressl=yes&ip=58.182.53.141&pl=21&id=o-ALuhu_QbWSF_PEtGHmJNJKjWFhpGN9WSshIYzOL2iy8c&fexp=900718%2C904848%2C907263%2C913441%2C927622%2C930676%2C936122%2C9406282%2C941004%2C942618%2C943917%2C947225%2C948124%2C949427%2C952302%2C952605%2C952901%2C955301%2C957103%2C957105%2C957201%2C959701&mm=31&expire=1422387730&sver=3&dur=99.200&ipbits=0&key=yt5&gir=yes&mime=video%2Fmp4&signature=4860278ECB1825227CF8441FFB3FAE991FEC906C.BDB09CE988A567F3E478A955009A910A057AE0E3&clen=3053553&itag=133&source=youtube&upn=_H6K7YDb4ms&initcwndbps=1371250&keepalive=yes&ratebypass=yes', u'format_note': u'DASH video', u'player_url': None, u'ext': u'mp4', u'preference': -10040, u'format_id': u'nondash-133', u'height': 240, u'acodec': u'none'}, {u'format': u'nondash-243 - 360p (DASH video)', u'url': u'https://r3---sn-nu5gi0c-npos.googlevideo.com/videoplayback?ms=au&lmt=1420637054819442&mv=m&sparams=clen%2Cdur%2Cgir%2Cid%2Cinitcwndbps%2Cip%2Cipbits%2Citag%2Ckeepalive%2Clmt%2Cmime%2Cmm%2Cms%2Cmv%2Cpl%2Crequiressl%2Csource%2Cupn%2Cexpire&mt=1422366034&requiressl=yes&ip=58.182.53.141&pl=21&id=o-ALuhu_QbWSF_PEtGHmJNJKjWFhpGN9WSshIYzOL2iy8c&fexp=900718%2C904848%2C907263%2C913441%2C927622%2C930676%2C936122%2C9406282%2C941004%2C942618%2C943917%2C947225%2C948124%2C949427%2C952302%2C952605%2C952901%2C955301%2C957103%2C957105%2C957201%2C959701&mm=31&expire=1422387730&sver=3&dur=99.200&ipbits=0&key=yt5&gir=yes&mime=video%2Fwebm&signature=542B9DAE178A51AF8FBE61F1F42273E898C1392B.D215B04EBCD5561CDBDE5567B5CAA4078FDC9025&clen=4765207&itag=243&source=youtube&upn=_H6K7YDb4ms&initcwndbps=1371250&keepalive=yes&ratebypass=yes', u'format_note': u'DASH video', u'player_url': None, u'ext': u'webm', u'preference': -10040, u'format_id': u'nondash-243', u'height': 360, u'acodec': u'none'}, {u'format': u'nondash-134 - 360p (DASH video)', u'url': u'https://r3---sn-nu5gi0c-npos.googlevideo.com/videoplayback?ms=au&lmt=1421241676779457&mv=m&sparams=clen%2Cdur%2Cgir%2Cid%2Cinitcwndbps%2Cip%2Cipbits%2Citag%2Ckeepalive%2Clmt%2Cmime%2Cmm%2Cms%2Cmv%2Cpl%2Crequiressl%2Csource%2Cupn%2Cexpire&mt=1422366034&requiressl=yes&ip=58.182.53.141&pl=21&id=o-ALuhu_QbWSF_PEtGHmJNJKjWFhpGN9WSshIYzOL2iy8c&fexp=900718%2C904848%2C907263%2C913441%2C927622%2C930676%2C936122%2C9406282%2C941004%2C942618%2C943917%2C947225%2C948124%2C949427%2C952302%2C952605%2C952901%2C955301%2C957103%2C957105%2C957201%2C959701&mm=31&expire=1422387730&sver=3&dur=99.200&ipbits=0&key=yt5&gir=yes&mime=video%2Fmp4&signature=3EA1FB1EBF3904A3A7F1678C0A36DFE7FEE8F5B7.E25E93B35B6D597F891EF2904CDC6643227307AD&clen=5675638&itag=134&source=youtube&upn=_H6K7YDb4ms&initcwndbps=1371250&keepalive=yes&ratebypass=yes', u'format_note': u'DASH video', u'player_url': None, u'ext': u'mp4', u'preference': -10040, u'format_id': u'nondash-134', u'height': 360, u'acodec': u'none'}, {u'format': u'nondash-244 - 480p (DASH video)', u'url': u'https://r3---sn-nu5gi0c-npos.googlevideo.com/videoplayback?ms=au&lmt=1420637070231033&mv=m&sparams=clen%2Cdur%2Cgir%2Cid%2Cinitcwndbps%2Cip%2Cipbits%2Citag%2Ckeepalive%2Clmt%2Cmime%2Cmm%2Cms%2Cmv%2Cpl%2Crequiressl%2Csource%2Cupn%2Cexpire&mt=1422366034&requiressl=yes&ip=58.182.53.141&pl=21&id=o-ALuhu_QbWSF_PEtGHmJNJKjWFhpGN9WSshIYzOL2iy8c&fexp=900718%2C904848%2C907263%2C913441%2C927622%2C930676%2C936122%2C9406282%2C941004%2C942618%2C943917%2C947225%2C948124%2C949427%2C952302%2C952605%2C952901%2C955301%2C957103%2C957105%2C957201%2C959701&mm=31&expire=1422387730&sver=3&dur=99.200&ipbits=0&key=yt5&gir=yes&mime=video%2Fwebm&signature=3A80EBA510746DCC22A70312F2243E5719CC3534.1CAD46920CC17D4C691A60C20891B2B86F97EDEB&clen=8371402&itag=244&source=youtube&upn=_H6K7YDb4ms&initcwndbps=1371250&keepalive=yes&ratebypass=yes', u'format_note': u'DASH video', u'player_url': None, u'ext': u'webm', u'preference': -10040, u'format_id': u'nondash-244', u'height': 480, u'acodec': u'none'}, {u'format': u'nondash-135 - 480p (DASH video)', u'url': u'https://r3---sn-nu5gi0c-npos.googlevideo.com/videoplayback?ms=au&lmt=1421241693130145&mv=m&sparams=clen%2Cdur%2Cgir%2Cid%2Cinitcwndbps%2Cip%2Cipbits%2Citag%2Ckeepalive%2Clmt%2Cmime%2Cmm%2Cms%2Cmv%2Cpl%2Crequiressl%2Csource%2Cupn%2Cexpire&mt=1422366034&requiressl=yes&ip=58.182.53.141&pl=21&id=o-ALuhu_QbWSF_PEtGHmJNJKjWFhpGN9WSshIYzOL2iy8c&fexp=900718%2C904848%2C907263%2C913441%2C927622%2C930676%2C936122%2C9406282%2C941004%2C942618%2C943917%2C947225%2C948124%2C949427%2C952302%2C952605%2C952901%2C955301%2C957103%2C957105%2C957201%2C959701&mm=31&expire=1422387730&sver=3&dur=99.200&ipbits=0&key=yt5&gir=yes&mime=video%2Fmp4&signature=7811F2C2C8D5E161C3E94E6373E42531D735AFA1.F094222C079E01194EC11EAD2EC2C811C050FCED&clen=10706792&itag=135&source=youtube&upn=_H6K7YDb4ms&initcwndbps=1371250&keepalive=yes&ratebypass=yes', u'format_note': u'DASH video', u'player_url': None, u'ext': u'mp4', u'preference': -10040, u'format_id': u'nondash-135', u'height': 480, u'acodec': u'none'}, {u'asr': 44100, u'tbr': 92, u'format': u'171 - audio only (DASH audio)', u'format_note': u'DASH audio', u'height': None, u'preference': -50, u'format_id': '171', u'url': 'https://r3---sn-nu5gi0c-npos.googlevideo.com/videoplayback?id=6465c3e706e2c5b1&itag=171&source=youtube&requiressl=yes&ms=au&mv=m&pl=21&mm=31&ratebypass=yes&mime=audio/webm&gir=yes&clen=885873&lmt=1420637006451010&dur=99.241&signature=8BBB7E9B0743F257BA161029E3A6282DF00D9007.5FA8D6FA0C372E8514D58D0B4F4B4B4D57D2C1CA&key=dg_yt0&mt=1422366034&upn=_H6K7YDb4ms&sver=3&fexp=900718,904848,907263,913441,927622,930676,936122,9406282,941004,942618,943917,947225,948124,949427,952302,952605,952901,955301,957103,957105,957201,959701&ip=58.182.53.141&ipbits=0&expire=1422387730&sparams=ip,ipbits,expire,id,itag,source,requiressl,ms,mv,pl,mm,ratebypass,mime,gir,clen,lmt,dur', u'vcodec': u'none', u'abr': 128, u'width': None, u'ext': u'webm', u'filesize': 885873, u'fps': None}, {u'asr': 44100, u'tbr': 129, u'format': u'140 - audio only (DASH audio)', u'format_note': u'DASH audio', u'height': None, u'preference': -50, u'format_id': '140', u'container': u'm4a_dash', u'url': 'https://r3---sn-nu5gi0c-npos.googlevideo.com/videoplayback?id=6465c3e706e2c5b1&itag=140&source=youtube&requiressl=yes&ms=au&mv=m&pl=21&mm=31&ratebypass=yes&mime=audio/mp4&gir=yes&clen=1594596&lmt=1421241656406916&dur=99.287&signature=2B64A08FC55F67B50ADE86400B3AFC2C7EC573F7.2C34BBFC8EA58BE9C26B9891A93AC09551FAFFE0&key=dg_yt0&mt=1422366034&upn=_H6K7YDb4ms&sver=3&fexp=900718,904848,907263,913441,927622,930676,936122,9406282,941004,942618,943917,947225,948124,949427,952302,952605,952901,955301,957103,957105,957201,959701&ip=58.182.53.141&ipbits=0&expire=1422387730&sparams=ip,ipbits,expire,id,itag,source,requiressl,ms,mv,pl,mm,ratebypass,mime,gir,clen,lmt,dur', u'vcodec': u'none', u'abr': 128, u'width': None, u'ext': u'm4a', u'filesize': 1594596, u'fps': None, u'acodec': u'aac'}, {u'asr': 44100, u'tbr': 255, u'format': u'141 - audio only (DASH audio)', u'format_note': u'DASH audio', u'height': None, u'preference': -50, u'format_id': '141', u'container': u'm4a_dash', u'url': 'https://r3---sn-nu5gi0c-npos.googlevideo.com/videoplayback?id=6465c3e706e2c5b1&itag=141&source=youtube&requiressl=yes&ms=au&mv=m&pl=21&mm=31&ratebypass=yes&mime=audio/mp4&gir=yes&clen=3166148&lmt=1421241654735444&dur=99.288&signature=848CA838AED18AB2AD253FB95D610B17154C6199.601568AF5C5C5C2B334D69842E9AA69DDFC94A77&key=dg_yt0&mt=1422366034&upn=_H6K7YDb4ms&sver=3&fexp=900718,904848,907263,913441,927622,930676,936122,9406282,941004,942618,943917,947225,948124,949427,952302,952605,952901,955301,957103,957105,957201,959701&ip=58.182.53.141&ipbits=0&expire=1422387730&sparams=ip,ipbits,expire,id,itag,source,requiressl,ms,mv,pl,mm,ratebypass,mime,gir,clen,lmt,dur', u'vcodec': u'none', u'abr': 256, u'width': None, u'ext': u'm4a', u'filesize': 3166148, u'fps': None, u'acodec': u'aac'}, {u'asr': None, u'tbr': 107, u'format': u'278 - 256x144 (DASH video)', u'format_note': u'DASH video', u'height': 144, u'preference': -40, u'format_id': '278', u'container': u'webm', u'url': 'https://r3---sn-nu5gi0c-npos.googlevideo.com/videoplayback?id=6465c3e706e2c5b1&itag=278&source=youtube&requiressl=yes&ms=au&mv=m&pl=21&mm=31&ratebypass=yes&mime=video/webm&gir=yes&clen=1096555&lmt=1420637063505350&dur=99.200&signature=8ED9723B18E438558747595AB40739EF715278F6.6438AC11988C2DDB5F508D7B1DD69FF6D767696B&key=dg_yt0&mt=1422366034&upn=_H6K7YDb4ms&sver=3&fexp=900718,904848,907263,913441,927622,930676,936122,9406282,941004,942618,943917,947225,948124,949427,952302,952605,952901,955301,957103,957105,957201,959701&ip=58.182.53.141&ipbits=0&expire=1422387730&sparams=ip,ipbits,expire,id,itag,source,requiressl,ms,mv,pl,mm,ratebypass,mime,gir,clen,lmt,dur', u'vcodec': u'VP9', u'width': 256, u'ext': u'webm', u'filesize': 1096555, u'fps': 13, u'acodec': u'none'}, {u'asr': None, u'tbr': 120, u'format': u'160 - 256x144 (DASH video)', u'format_note': u'DASH video', u'height': 144, u'preference': -40, u'format_id': '160', u'url': 'https://r3---sn-nu5gi0c-npos.googlevideo.com/videoplayback?id=6465c3e706e2c5b1&itag=160&source=youtube&requiressl=yes&ms=au&mv=m&pl=21&mm=31&ratebypass=yes&mime=video/mp4&gir=yes&clen=1376770&lmt=1421241656835610&dur=99.280&signature=8CF37FE9647D592D20068A116097D2B1A887872D.3155F7973FA8AC4FC274CF89305573EF87E1EAD7&key=dg_yt0&mt=1422366034&upn=_H6K7YDb4ms&sver=3&fexp=900718,904848,907263,913441,927622,930676,936122,9406282,941004,942618,943917,947225,948124,949427,952302,952605,952901,955301,957103,957105,957201,959701&ip=58.182.53.141&ipbits=0&expire=1422387730&sparams=ip,ipbits,expire,id,itag,source,requiressl,ms,mv,pl,mm,ratebypass,mime,gir,clen,lmt,dur', u'width': 256, u'ext': u'mp4', u'filesize': 1376770, u'fps': 13, u'acodec': u'none'}, {u'asr': None, u'tbr': 259, u'format': u'242 - 426x240 (DASH video)', u'format_note': u'DASH video', u'height': 240, u'preference': -40, u'format_id': '242', u'url': 'https://r3---sn-nu5gi0c-npos.googlevideo.com/videoplayback?id=6465c3e706e2c5b1&itag=242&source=youtube&requiressl=yes&ms=au&mv=m&pl=21&mm=31&ratebypass=yes&mime=video/webm&gir=yes&clen=2563832&lmt=1420637040489362&dur=99.200&signature=334CBB83122C8CA8650F181CB5CB4DB98E1B0FE0.5DD560E4793A46E5052EB513EBA50CF9C720F363&key=dg_yt0&mt=1422366034&upn=_H6K7YDb4ms&sver=3&fexp=900718,904848,907263,913441,927622,930676,936122,9406282,941004,942618,943917,947225,948124,949427,952302,952605,952901,955301,957103,957105,957201,959701&ip=58.182.53.141&ipbits=0&expire=1422387730&sparams=ip,ipbits,expire,id,itag,source,requiressl,ms,mv,pl,mm,ratebypass,mime,gir,clen,lmt,dur', u'width': 426, u'ext': u'webm', u'filesize': 2563832, u'fps': 25, u'acodec': u'none'}, {u'asr': None, u'tbr': 260, u'format': u'133 - 426x240 (DASH video)', u'format_note': u'DASH video', u'height': 240, u'preference': -40, u'format_id': '133', u'url': 'https://r3---sn-nu5gi0c-npos.googlevideo.com/videoplayback?id=6465c3e706e2c5b1&itag=133&source=youtube&requiressl=yes&ms=au&mv=m&pl=21&mm=31&ratebypass=yes&mime=video/mp4&gir=yes&clen=3053553&lmt=1421241659705814&dur=99.200&signature=771BD514B7DBB863145C27D07B8D70AE91E600F5.643A6B823B2A4B5B2CA655DF54F6F6337C9EA6E7&key=dg_yt0&mt=1422366034&upn=_H6K7YDb4ms&sver=3&fexp=900718,904848,907263,913441,927622,930676,936122,9406282,941004,942618,943917,947225,948124,949427,952302,952605,952901,955301,957103,957105,957201,959701&ip=58.182.53.141&ipbits=0&expire=1422387730&sparams=ip,ipbits,expire,id,itag,source,requiressl,ms,mv,pl,mm,ratebypass,mime,gir,clen,lmt,dur', u'width': 426, u'ext': u'mp4', u'filesize': 3053553, u'fps': 25, u'acodec': u'none'}, {u'asr': None, u'tbr': 482, u'format': u'243 - 640x360 (DASH video)', u'format_note': u'DASH video', u'height': 360, u'preference': -40, u'format_id': '243', u'url': 'https://r3---sn-nu5gi0c-npos.googlevideo.com/videoplayback?id=6465c3e706e2c5b1&itag=243&source=youtube&requiressl=yes&ms=au&mv=m&pl=21&mm=31&ratebypass=yes&mime=video/webm&gir=yes&clen=4765207&lmt=1420637054819442&dur=99.200&signature=3016B507220587B779ADC3CABF84FC92DD5E5F5D.939B25316B44F27DAC6DD8EE8462A293859DE69E&key=dg_yt0&mt=1422366034&upn=_H6K7YDb4ms&sver=3&fexp=900718,904848,907263,913441,927622,930676,936122,9406282,941004,942618,943917,947225,948124,949427,952302,952605,952901,955301,957103,957105,957201,959701&ip=58.182.53.141&ipbits=0&expire=1422387730&sparams=ip,ipbits,expire,id,itag,source,requiressl,ms,mv,pl,mm,ratebypass,mime,gir,clen,lmt,dur', u'width': 640, u'ext': u'webm', u'filesize': 4765207, u'fps': 25, u'acodec': u'none'}, {u'asr': None, u'tbr': 608, u'format': u'134 - 640x360 (DASH video)', u'format_note': u'DASH video', u'height': 360, u'preference': -40, u'format_id': '134', u'url': 'https://r3---sn-nu5gi0c-npos.googlevideo.com/videoplayback?id=6465c3e706e2c5b1&itag=134&source=youtube&requiressl=yes&ms=au&mv=m&pl=21&mm=31&ratebypass=yes&mime=video/mp4&gir=yes&clen=5675638&lmt=1421241676779457&dur=99.200&signature=615F55C0BED63DBBCD9881114737B91B7C1EDB37.5C81AA884B813099A1414DE76FE7FF2A5E1C73A7&key=dg_yt0&mt=1422366034&upn=_H6K7YDb4ms&sver=3&fexp=900718,904848,907263,913441,927622,930676,936122,9406282,941004,942618,943917,947225,948124,949427,952302,952605,952901,955301,957103,957105,957201,959701&ip=58.182.53.141&ipbits=0&expire=1422387730&sparams=ip,ipbits,expire,id,itag,source,requiressl,ms,mv,pl,mm,ratebypass,mime,gir,clen,lmt,dur', u'width': 640, u'ext': u'mp4', u'filesize': 5675638, u'fps': 25, u'acodec': u'none'}, {u'asr': None, u'tbr': 854, u'format': u'244 - 854x480 (DASH video)', u'format_note': u'DASH video', u'height': 480, u'preference': -40, u'format_id': '244', u'url': 'https://r3---sn-nu5gi0c-npos.googlevideo.com/videoplayback?id=6465c3e706e2c5b1&itag=244&source=youtube&requiressl=yes&ms=au&mv=m&pl=21&mm=31&ratebypass=yes&mime=video/webm&gir=yes&clen=8371402&lmt=1420637070231033&dur=99.200&signature=684EA85031901276A3E4FB19BC355873E89712E3.36E16124966A868F4947177A1785B4DDE30E0C46&key=dg_yt0&mt=1422366034&upn=_H6K7YDb4ms&sver=3&fexp=900718,904848,907263,913441,927622,930676,936122,9406282,941004,942618,943917,947225,948124,949427,952302,952605,952901,955301,957103,957105,957201,959701&ip=58.182.53.141&ipbits=0&expire=1422387730&sparams=ip,ipbits,expire,id,itag,source,requiressl,ms,mv,pl,mm,ratebypass,mime,gir,clen,lmt,dur', u'width': 854, u'ext': u'webm', u'filesize': 8371402, u'fps': 25, u'acodec': u'none'}, {u'asr': None, u'tbr': 1113, u'format': u'135 - 854x480 (DASH video)', u'format_note': u'DASH video', u'height': 480, u'preference': -40, u'format_id': '135', u'url': 'https://r3---sn-nu5gi0c-npos.googlevideo.com/videoplayback?id=6465c3e706e2c5b1&itag=135&source=youtube&requiressl=yes&ms=au&mv=m&pl=21&mm=31&ratebypass=yes&mime=video/mp4&gir=yes&clen=10706792&lmt=1421241693130145&dur=99.200&signature=4AFD3FBF3F9A81A5AE8D20D26C77604DD3B971CD.765A24ED4BC8FE5821518781CBD3F74092DCE6C5&key=dg_yt0&mt=1422366034&upn=_H6K7YDb4ms&sver=3&fexp=900718,904848,907263,913441,927622,930676,936122,9406282,941004,942618,943917,947225,948124,949427,952302,952605,952901,955301,957103,957105,957201,959701&ip=58.182.53.141&ipbits=0&expire=1422387730&sparams=ip,ipbits,expire,id,itag,source,requiressl,ms,mv,pl,mm,ratebypass,mime,gir,clen,lmt,dur', u'width': 854, u'ext': u'mp4', u'filesize': 10706792, u'fps': 25, u'acodec': u'none'}, {u'width': 176, u'ext': u'3gp', u'format': u'17 - 176x144', u'url': u'https://r3---sn-nu5gi0c-npos.googlevideo.com/videoplayback?signature=720CEE5DBA06BF44A48BC9DEF09B1F3F9474BE3D.A3E8CC09A80C3A13821DD67CF57ABF5E0F46D3CE&ms=au&mime=video%2F3gpp&mv=m&sparams=dur%2Cid%2Cinitcwndbps%2Cip%2Cipbits%2Citag%2Cmime%2Cmm%2Cms%2Cmv%2Cpl%2Crequiressl%2Csource%2Cupn%2Cexpire&source=youtube&upn=_H6K7YDb4ms&initcwndbps=1371250&requiressl=yes&ip=58.182.53.141&itag=17&mt=1422366034&expire=1422387730&key=yt5&sver=3&pl=21&id=o-ALuhu_QbWSF_PEtGHmJNJKjWFhpGN9WSshIYzOL2iy8c&fexp=900718%2C904848%2C907263%2C913441%2C927622%2C930676%2C936122%2C9406282%2C941004%2C942618%2C943917%2C947225%2C948124%2C949427%2C952302%2C952605%2C952901%2C955301%2C957103%2C957105%2C957201%2C959701&dur=99.474&ipbits=0&mm=31&ratebypass=yes', u'format_id': u'17', u'height': 144, u'player_url': None}, {u'width': 320, u'ext': u'3gp', u'format': u'36 - 320x240', u'url': u'https://r3---sn-nu5gi0c-npos.googlevideo.com/videoplayback?signature=DDD28CD3A9A3805EA413B3EA6BFD31C3E80F41BF.22BE934A799926E5C93FE6AA77B1645FA44EA7EC&ms=au&mime=video%2F3gpp&mv=m&sparams=dur%2Cid%2Cinitcwndbps%2Cip%2Cipbits%2Citag%2Cmime%2Cmm%2Cms%2Cmv%2Cpl%2Crequiressl%2Csource%2Cupn%2Cexpire&source=youtube&upn=_H6K7YDb4ms&initcwndbps=1371250&requiressl=yes&ip=58.182.53.141&itag=36&mt=1422366034&expire=1422387730&key=yt5&sver=3&pl=21&id=o-ALuhu_QbWSF_PEtGHmJNJKjWFhpGN9WSshIYzOL2iy8c&fexp=900718%2C904848%2C907263%2C913441%2C927622%2C930676%2C936122%2C9406282%2C941004%2C942618%2C943917%2C947225%2C948124%2C949427%2C952302%2C952605%2C952901%2C955301%2C957103%2C957105%2C957201%2C959701&dur=99.427&ipbits=0&mm=31&ratebypass=yes', u'format_id': u'36', u'height': 240, u'player_url': None}, {u'width': 400, u'ext': u'flv', u'format': u'5 - 400x240', u'url': u'https://r3---sn-nu5gi0c-npos.googlevideo.com/videoplayback?signature=88B9EE78B7DD9B098BD74D53C38389BC7C9183FB.23400135A9A95F66C288E9EB31A1D255A1200092&ms=au&mime=video%2Fx-flv&mv=m&sparams=dur%2Cid%2Cinitcwndbps%2Cip%2Cipbits%2Citag%2Cmime%2Cmm%2Cms%2Cmv%2Cpl%2Crequiressl%2Csource%2Cupn%2Cexpire&source=youtube&upn=_H6K7YDb4ms&initcwndbps=1371250&requiressl=yes&ip=58.182.53.141&itag=5&mt=1422366034&expire=1422387730&key=yt5&sver=3&pl=21&id=o-ALuhu_QbWSF_PEtGHmJNJKjWFhpGN9WSshIYzOL2iy8c&fexp=900718%2C904848%2C907263%2C913441%2C927622%2C930676%2C936122%2C9406282%2C941004%2C942618%2C943917%2C947225%2C948124%2C949427%2C952302%2C952605%2C952901%2C955301%2C957103%2C957105%2C957201%2C959701&dur=99.291&ipbits=0&mm=31&ratebypass=yes', u'format_id': u'5', u'height': 240, u'player_url': None}, {u'width': 640, u'ext': u'webm', u'format': u'43 - 640x360', u'url': u'https://r3---sn-nu5gi0c-npos.googlevideo.com/videoplayback?ms=au&mv=m&sparams=dur%2Cid%2Cinitcwndbps%2Cip%2Cipbits%2Citag%2Cmime%2Cmm%2Cms%2Cmv%2Cpl%2Cratebypass%2Crequiressl%2Csource%2Cupn%2Cexpire&mt=1422366034&requiressl=yes&ip=58.182.53.141&pl=21&id=o-ALuhu_QbWSF_PEtGHmJNJKjWFhpGN9WSshIYzOL2iy8c&fexp=900718%2C904848%2C907263%2C913441%2C927622%2C930676%2C936122%2C9406282%2C941004%2C942618%2C943917%2C947225%2C948124%2C949427%2C952302%2C952605%2C952901%2C955301%2C957103%2C957105%2C957201%2C959701&mm=31&expire=1422387730&ratebypass=yes&sver=3&dur=0.000&ipbits=0&key=yt5&mime=video%2Fwebm&signature=65FD39C2D8C3E857410958674E3EDB73D290DDA8.BB72F643FACC7D0BCF5028965E499955A4DFD051&itag=43&source=youtube&upn=_H6K7YDb4ms&initcwndbps=1371250', u'format_id': u'43', u'height': 360, u'player_url': None}, {u'width': 640, u'ext': u'mp4', u'format': u'18 - 640x360', u'url': u'https://r3---sn-nu5gi0c-npos.googlevideo.com/videoplayback?ms=au&mv=m&sparams=dur%2Cid%2Cinitcwndbps%2Cip%2Cipbits%2Citag%2Cmime%2Cmm%2Cms%2Cmv%2Cpl%2Cratebypass%2Crequiressl%2Csource%2Cupn%2Cexpire&mt=1422366034&requiressl=yes&ip=58.182.53.141&pl=21&id=o-ALuhu_QbWSF_PEtGHmJNJKjWFhpGN9WSshIYzOL2iy8c&fexp=900718%2C904848%2C907263%2C913441%2C927622%2C930676%2C936122%2C9406282%2C941004%2C942618%2C943917%2C947225%2C948124%2C949427%2C952302%2C952605%2C952901%2C955301%2C957103%2C957105%2C957201%2C959701&mm=31&expire=1422387730&ratebypass=yes&sver=3&dur=99.288&ipbits=0&key=yt5&mime=video%2Fmp4&signature=A52E7B908AAEFEC7EB23299B38D6DA995A711FA0.4BBB59E2B7614E646BD570A6CD7FCA79478CAC32&itag=18&source=youtube&upn=_H6K7YDb4ms&initcwndbps=1371250', u'format_id': u'18', u'height': 360, u'player_url': None}]}
    for key in sample:
        print key, ':', sample[key]

