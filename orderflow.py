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
    print COOKIE


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
def sendPostRequest(url, data, referer='https://kyfw.12306.cn/otn/index/init'):
    """"""
    pass


#----------------------------------------------------------------------
def sendGetRequest(url, referer='https://kyfw.12306.cn/otn/index/init'):
    """"""
    pass

#----------------------------------------------------------------------
def login(username, password, verifycode):
    """"""
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
               'Referer': 'https://kyfw.12306.cn/otn/login/init',
               'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
               'Connection': 'keep-alive',
               'Cookie': 'JSESSIONID=%s;BIGipServerotn=%s' % (COOKIE['JSESSIONID'], COOKIE['BIGipServerotn'])}
    
    params = {'randCode': verifycode, 'rand': 'sjrand'}
    #验证码验证
    print params['randCode']
    print headers
    resp, content = http.request(uri = 'https://kyfw.12306.cn/otn/passcodeNew/checkRandCodeAnsyn',
                                 method = 'POST', 
                                 body= urllib.urlencode(params),
                                 headers = headers)
    
    data = json.loads(content)
    print data
    if data['data'] == 'N':
        return (False, u'验证码错误1')
    #点击登录按钮后 再次验证验证码
    resp, content = http.request(uri = 'https://kyfw.12306.cn/otn/passcodeNew/checkRandCodeAnsyn',
                                 method = 'POST', 
                                 body= urllib.urlencode(params),
                                 headers = headers)
    print data
    if data['data'] == 'N':
        return (False, u'验证码错误2')
    
    params = {'loginUserDTO.user_name': username,
              'userDTO.password': password,
              'randCode': verifycode}
    #登录验证
    resp, content = http.request(uri = 'https://kyfw.12306.cn/otn/login/loginAysnSuggest',
                                 method= 'POST',
                                 body= urllib.urlencode(params),
                                 headers = headers)
    data = json.loads(content)
    if data['data']['loginCheck'] != 'Y':
        return (False, u'登录验证失败')
    
    resp, content = http.request(uri = 'https://kyfw.12306.cn/otn/login/userLogin',
                                 method= 'POST',
                                 body = urllib.urlencode({'_json_att': ''}),
                                 headers = headers)
    if resp['status'] == '302':
        print 'login Ok'
        return (True, u'登录成功')
    else:
        return (Flase, u'登录失败')
    