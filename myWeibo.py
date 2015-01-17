from weibo import APIClient
from keyfile import *

# http://blog.hanxiaogang.com/weibo-data.html

import sys
import weibo
import webbrowser


def get_access_token():
    api = weibo.APIClient(APP_KEY, APP_SECRET)

    authorize_url = api.get_authorize_url(REDIRECT_URL)
    print(authorize_url)
    webbrowser.open_new(authorize_url)
    code = raw_input('authencation code: ')

    request = api.request_access_token(code, REDIRECT_URL)
    access_token = request.access_token
    expires_in = request.expires_in
    print 'access token: ', access_token
    print 'expire: ', expires_in


def get_data():
    access_token = '4af529b0cbe69d07a4dfddc29462d186'
    expires_in = '1579103224'
    api = weibo.APIClient(APP_KEY, APP_SECRET, redirect_uri=REDIRECT_URL)
    api.set_access_token(access_token, expires_in)
    r = api.status.home_timeline.get(uid=YOUR_USERID, count=100)
    return r.status


def save_data():
    conn = Connection()
    db = conn.tweets_db
    tweets_table = db.tweets_table
    tweets_table.ensure_index('id', unique=True)

    tweets = get_data()
    orignal_count = tweets_table.count()
    for tweet in tweets:
        tweets_table.update({'id': tweet['id']}, tweet, True)
    print 'added: ', tweets_table.count() - orignal_count


if __name__ == '__main__':
    # get_access_token()
    get_data()