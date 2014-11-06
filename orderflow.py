#! /usr/bin/env python
#-*-coding:utf8-*-

import httplib2
import logging
import urllib
import json

from os import makedirs
from os.path import isdir, dirname
from random import random
from os import makedirs
from os.path import isdir, dirname

logging.basicConfig(filename='log.txt',format='%(asctime)s %(message)s -->',datefmt='%Y/%m/%d %I:%M:%S',level=logging.INFO)


COOKIE = {
          'JSESSIONID': '',
          'BIGipServerotn': '',
          }

http = httplib2.Http(timeout= 5, disable_ssl_certificate_validation= True)

#----------------------------------------------------------------------
def init():
    """"""
    headers = {'Host': 'kyfw.12306.cn',
               'Connection': 'keep-alive',}
    resp, content = http.request('https://kyfw.12306.cn/otn/login/init', headers = headers)
    COOKIE['JSESSIONID'] = resp['set-cookie'].split(',')[0].split(';')[0].split('=')[1]
    COOKIE['BIGipServerotn'] = resp['set-cookie'].split(',')[1].split(';')[0].split('=')[1]


#----------------------------------------------------------------------
def getVerifyCode(isfirst = False):
    """"""
    filename = 'verifyCode/getPassCodeNew.png'
    dir1 = dirname(filename)
    if not isdir(dir1):
        makedirs(dir1)
    if not isfirst:
        url = 'https://kyfw.12306.cn/otn/passcodeNew/getPassCodeNew?module=login&rand=sjrand&%.17s' % random()
        try:
            urllib.urlretrieve(url,filename)
            return filename
        except:
            return None
            
    else:
        url = 'https://kyfw.12306.cn/otn/passcodeNew/getPassCodeNew;jsessionid=%s?module=login&rand=sjrand' % COOKIE['JSESSIONID']
        try:
            print url
            urllib.urlretrieve(url,filename)
            return filename
        except:
            return None

#----------------------------------------------------------------------
def queryTrainNo():
    """"""
    pass



#----------------------------------------------------------------------
def queryPassengers():
    """"""
    pass


#----------------------------------------------------------------------
def login(username, password, verifycode):
    """"""
    headers = {'Host': 'kyfw.12306.cn',
               'Origin': 'https://kyfw.12306.cn',
               'Referer': 'https://kyfw.12306.cn/otn/login/init',
               'Connection': 'keep-alive',}
    
    params = {'randCode': verifycode, 'rand': 'sjrand'}
    resp, content = http.request(uri = 'https://kyfw.12306.cn/otn/passcodeNew/checkRandCodeAnsyn',
                                 method = 'POST', 
                                 body= urllib.urlencode(params),
                                 headers = headers)
    
    data = json.loads(content)
    print data
    if data['data'] == 'N':
        return (False, u'验证码错误')
    resp, content = http.request(uri = 'https://kyfw.12306.cn/otn')
    
    