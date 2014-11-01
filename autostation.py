#-*-coding:utf8-*-

import os

#_STATION_PATH=r"D:\github\tickets\stations"
_STATION_PATH="./stations"

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
	names=['a','b','c','d','e','f']
	try:
		with open(path,'rb') as f:
			L=f.read().strip().split('@')
		if L is not None:
			return [Dict(names,x.split('|')) for x in L]
		else:
			return None
	except:
		raise

def stationQuery(letter):
	result=[]
	for line in parseStationList():
		if line.e.startswith(letter.lower()):
			result.append(line)
	if len(result):
		return sorted(result)

if __name__ == '__main__':
	for i in stationQuery('gzd'):
		with open('./test.txt','a') as f:
			f.write(i.b+'\n')

