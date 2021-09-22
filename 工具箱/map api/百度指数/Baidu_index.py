#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: wild_orange
# @Email: jixuanfan_seu@163.com
# @Date:   2020-07-21 22:20:06
# @Last Modified time: 2020-10-25 19:39:31

import requests
import datetime
import time
import json

headers={'User-Agent': 'Chrome/76.0.3809.132'}
base_url='http://index.baidu.com/'

cookies={'cookie':'[BIDUPSID=3E6941CAAF7046CCB333A788DC2768D7; PSTM=1574166263; BDUSS=hodWk1M092c3NXTH5WT2J6dXBzTUczamhnLTZ5NzE2WnZlMTJxNXFtSjJ5UVZlRVFBQUFBJCQAAAAAAAAAAAEAAACzKA8Wz~TB-lkAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHY83l12PN5dOT; MCITY=-340%3A; BAIDUID=21685965964C1D9D27D9A517462B3B71:FG=1; delPer=0; PSINO=7; H_PS_PSSID=1466_33223_33061_31253_32974_33098_33101_32938_33218_33199_33145_33149_22157; BA_HECTOR=81850g852h24ag0lfn1ftcb060r; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc=1607871497; Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc=1607871497; __yjsv5_shitong=1.0_7_6cbca2e2e65c6ca4e7b9f669be80f090429c_300_1607871498786_219.223.233.98_f8a7d616; bdindexid=bn2jcu99pi2jeu1s377bvo9hl1; RT="z=1&dm=baidu.com&si=64x5y7l3kd9&ss=kin96a99&sl=2&tt=3q0&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=3qo&ul=guv"]'} #这里填写你自己的cookie

# 加载区域编码文件
index_file='baidu_index_code.csv'
with open(index_file,encoding='utf-8') as f:
	data=[x.strip().split(',') for x in f.readlines()]
	r_codes={x[1]:x[0] for x in data}
	codes={x[0]:x[1] for x in data}

def decrypt(t,e):
	n, i, a, result = list(t), list(e), {}, []
	ln = int(len(n)/2)
	start, end = n[ln:], n[:ln]
	a = dict(zip(end, start))
	return ''.join([a[j] for j in e])

def get_ptbk(uniqid):
	url=base_url+'Interface/ptbk?uniqid=%s'%uniqid
	res=requests.get(url,headers=headers,cookies=cookies)
	if res.status_code==200:
		ptbk=res.json()['data']
		return ptbk
	else:
		print('uniqid获取失败~状态码为：%s'%res.status_code)
		return None

def parse_date(start,end):
	START=datetime.datetime.strptime(start,'%Y-%m-%d')
	END=datetime.datetime.strptime(end,'%Y-%m-%d')
	BEGIN=datetime.datetime.strptime('2011-01-01','%Y-%m-%d') #百度指数能查到的最早日期
	LAST=datetime.datetime.today()-datetime.timedelta(days=1) #百度指数能查到的最晚日期
	if START<BEGIN: START=BEGIN
	if END>LAST: END=LAST
	delta_days=(END-START).days
	if delta_days<0:
		print('开始日期不能晚于结束日期！')
		return None
	START_STR=START.strftime('%Y-%m-%d')

	BATCH=360 #每次提取BATCH天数据，若查询的时间范围超过一年，则百度指数返回以周为周期的数据
	retVal=[]
	curDate=END
	curPreDate=curDate-datetime.timedelta(days=BATCH)
	curPreDate_str=curPreDate.strftime('%Y-%m-%d')
	curDate_str=curDate.strftime('%Y-%m-%d')
	retVal.append([START_STR if curPreDate<START else curPreDate_str,curDate_str])
	curDate=curPreDate-datetime.timedelta(days=1)
	while curDate>START:
		curPreDate=curDate-datetime.timedelta(days=BATCH)
		curPreDate_str=curPreDate.strftime('%Y-%m-%d')
		curDate_str=curDate.strftime('%Y-%m-%d')
		retVal.append([START_STR if curPreDate<START else curPreDate_str,curDate_str])
		curDate=curPreDate-datetime.timedelta(days=1)
	retVal=retVal[::-1] #逆序转换
	return retVal

def Baidu_index(keyword,start,end,area='0',fmt='L'):
	'''
		@param:
			keyword: str, 需要查询的词汇
			start：str, 开始时间，'20XX-XX-XX'格式，不能早于2011-01-01
			end：str，结束时间，20XX-XX-XX'格式，不能晚于前一天时间
			area：int/str, 区域编码或者名称，需要提前在baidu_index_code.csv文件中配置（目前已配置全国、省、江苏地级市)
			fmt: 'L'或'D', 返回值格式，分别表示数组格式(List)和字典格式(Dict)。
		@output:
			若fmt为'L'，返回一个二维数组，每一行表示：日期字符串, PC+移动端数据, PC端数据, 移动端数据。按时间先后顺序排序。
			若fmt为'D'，返回一个字典，共有4个key-value：
					period: list, [开始日期字符串，结束日期字符串]
					all: list of int, PC+移动端数据, 按时间先后顺序排序
					pc: list of int, PC端数据, 按时间先后顺序排序
					mobile: list of int, 移动端数据, 按时间先后顺序排序
	'''
	area=str(area)
	if not area.isdigit():  #如果是区域名称（不是编码）
		if area not in r_codes.keys():
			print('区域编码文件中无%s的编码~'%area)
			return None
		else:
			code=r_codes[area]
	else:
		if area not in codes.keys():
			print('区域编码文件中无编码:%s'%area)
			return
		else:
			code=area

	dates=parse_date(start,end)
	if not dates: return None
	all_data=[]     #pc+移动端数据
	pc_data=[]      #pc端数据
	mobile_data=[]  #移动端数据
	for date in dates:
		print('正在查询%s%s至%s的数据'%(codes[code],date[0],date[1]))
		url=base_url+'api/SearchApi/index?area=%s&word=[[%%7B"name":"%s","wordType":1%%7D]]&startDate=%s&endDate=%s'%(code,keyword,date[0],date[1])
		res=requests.get(url,headers=headers,cookies=cookies)
		if res.status_code==200:
			data=res.json()['data']
			all_val=data['userIndexes'][0]['all']['data']
			pc_val=data['userIndexes'][0]['pc']['data']
			mobile_val=data['userIndexes'][0]['wise']['data']
			uniqid=data['uniqid']
			ptbk=get_ptbk(uniqid)
			all_data+=[int(x) if x else 0 for x in decrypt(ptbk,all_val).split(',')]
			pc_data+=[int(x) if x else 0 for x in decrypt(ptbk,pc_val).split(',')]
			mobile_data+=[int(x) if x else 0 for x in decrypt(ptbk,mobile_val).split(',')]
		else:
			print('数据获取失败~状态码为：%s'%res.status_code)
			return None
		time.sleep(3.5)
	if fmt=='L':
		START=datetime.datetime.strptime(dates[0][0],'%Y-%m-%d')
		END=datetime.datetime.strptime(dates[-1][1],'%Y-%m-%d')
		curDate=START
		all_dates_str=[]
		while curDate<=END:
			all_dates_str.append(curDate.strftime('%Y-%m-%d'))
			curDate+=datetime.timedelta(days=1)
			retVal=list(zip(all_dates_str,all_data,pc_data,mobile_data))
	elif fmt=='D':
		retVal={'period':[dates[0][0],dates[-1][1]],'all':all_data,'pc':pc_data,'mobile':mobile_data}
	else:
		print('fmt参数只能为L或D')
		retVal=None
	return retVal

def License():
	S='87/101/108/99/111/109/101/32/116/111/32/117/115/101/32/116/104/105/115/32/112/114/111/103/\
	114/97/109/33/10/65/117/116/104/111/114/58/32/68/101/99/111/100/101/10/72/111/109/101/112/97/\
	103/101/58/32/71/105/116/101/101/40/104/116/116/112/115/58/47/47/103/105/116/101/101/46/99/111/\
	109/47/106/105/120/117/97/110/102/97/110/41/10/32/32/32/32/32/32/32/32/32/32/67/83/68/78/40/104/\
	116/116/112/115/58/47/47/98/108/111/103/46/99/115/100/110/46/110/101/116/47/113/113/95/51/53/52/\
	48/56/48/51/48/41/10'
	print(''.join([chr(int(x)) for x in S.split('/')]))
License()

if __name__ == '__main__':
	START='2020-09-01'
	END='2020-10-01'
	data=Baidu_index('pycharm',START,END,'0')
	print(data)