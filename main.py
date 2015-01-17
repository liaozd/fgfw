#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '1.0'
__author__ = 'http://weibo.com/wtmmac'

'''
Demo for sinaweibopy
主要实现token自动生成及更新
适合于后端服务相关应用
'''

# api from:http://michaelliao.github.com/sinaweibopy/
from weibo import APIClient
import webbrowser
import sys, os, urllib, urllib2
from http_helper import *
from retry import *
from keyfile import *
try:
    import json
except ImportError:
    import simplejson as json

# setting sys encoding to utf-8
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

# token file path
save_access_token_file  = 'access_token.txt'
file_path = os.getcwd() + os.path.sep
access_token_file_path = file_path + save_access_token_file

client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)

def make_access_token():
    # api = weibo.APIClient(APP_KEY, APP_SECRET)

    authorize_url = client.get_authorize_url(REDIRECT_URL)
    print(authorize_url)
    webbrowser.open_new(authorize_url)
    code = raw_input('authencation code: ')

    request = client.request_access_token(code, REDIRECT_URL)
    access_token = request.access_token
    expires_in = request.expires_in
    print 'access token: ', access_token
    print 'expire: ', expires_in
    #得到token
    print request['access_token']
    save_access_token(request)

def save_access_token(request):
    '''将access token保存到本地'''
    f = open(access_token_file_path, 'w')
    f.write(request['access_token']+' ' + str(request['expires_in']))
    f.close()

@retry(1)
def apply_access_token():
    '''从本地读取及设置access token'''
    try:
        token = open(access_token_file_path, 'r').read().split()
        if len(token) != 2:
            make_access_token()
            return False
        # 过期验证
        access_token, expires_in = token
        try:
            client.set_access_token(access_token, expires_in)
        except StandardError, e:
            if hasattr(e, 'error'): 
                if e.error == 'expired_token':
                    # token过期重新生成
                    make_access_token()
            else:
                pass
    except:
        make_access_token()
    
    return False

if __name__ == "__main__":
    apply_access_token()

    # 以下为访问微博api的应用逻辑
    # 以接口访问状态为例
    status = client.get.account__rate_limit_status()
    print json.dumps(status)