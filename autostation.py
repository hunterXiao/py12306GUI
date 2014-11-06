#!/usr/bin/env python
#-*-coding:utf8-*-

import os
import sys
import logging

_STATION_PATH="./stations"

logging.basicConfig(filename='log.txt',format='%(asctime)s %(message)s -->',datefmt='%Y/%m/%d %I:%M:%S',level=logging.INFO)

class Dict(dict):
    """docstring for Dict"""
    def __init__(self, names=(),values=(),**kw):
        super(Dict, self).__init__(**kw)
        for k,v in zip(names,values):
            self[k]=v

    def __getattr__(self,key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError("Dict has no attribute '%s'"%key)

    def __setattr__(self,key,value):
        self[key]=value

#车站格式：bjb|北京北|VAP|beijingbei|bjb|0
def parseStationList(path=_STATION_PATH):
    L=None
    names=['abbr','name','telecode','pinyin','pyabbr']
    try:
        with open(path,'rb') as f:
            L=f.read().strip().split('@')
        if L is not None:
            return [Dict(names,x.split('|')[:5]) for x in L]
        else:
            return None
    except:
        logging.info(u'站点信息文件读取失败，程式退出')
        sys.exit()

def stationQuery(letter):
    result=[]
    for line in parseStationList():
        if line.pyabbr.startswith(letter.lower()) or line.pinyin.startswith(letter.lower()) or line.name.startswith(letter):
            result.append(line)
    if len(result):
        return sorted(result)