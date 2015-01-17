# -*- coding: utf-8 -*-
#/usr/bin/env python

import urllib2,cookielib


class SmartRedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_301(cls, req, fp, code, msg, headers):
        result = urllib2.HTTPRedirectHandler.http_error_301(cls, req, fp, code, msg, headers)
        result.status = code
        print headers
        return result

    def http_error_302(cls, req, fp, code, msg, headers):
        result = urllib2.HTTPRedirectHandler.http_error_302(cls, req, fp, code, msg, headers)
        result.status = code
        print headers
        return result

def get_cookie():
    cookies = cookielib.CookieJar()
    print cookies
    return urllib2.HTTPCookieProcessor(cookies)

def get_opener(proxy=False):
    rv=urllib2.build_opener(get_cookie(), SmartRedirectHandler())
    rv.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/39.0.2171.65 Chrome/39.0.2171.65 Safari/537.36')]
    return rv