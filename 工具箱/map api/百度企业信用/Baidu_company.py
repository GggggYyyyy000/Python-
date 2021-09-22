#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Wild Orange
# @Email: jixuanfan_seu@163.com
# @Date:   2020-06-19 22:38:14
# @Last Modified time: 2020-07-23 21:57:51

import requests
import re
import json

headers={'User-Agent': 'Chrome/76.0.3809.132'}

#正则表达式提取数据
re_get_js=re.compile(r'<script>([\s\S]*?)</script>')
re_resultList=re.compile(r'"resultList":(\[{.+?}\]),"totalNumFound')

def Get_company_info(name):
	'''
		@func: 通过百度企业信用查询企业基本信息
	'''
	url='https://xin.baidu.com/s?q=%s'%name
	res=requests.get(url,headers=headers)
	if res.status_code==200:
		html=res.text
		retVal=_parse_baidu_company_info(html)
		return retVal
	else:
		print('无法获取%s的企业信息'%name)

def _parse_baidu_company_info(html):
	'''
		@function：解析百度企业信用提供的企业基本信息
		@output: list of dict, [{},{},...]
			pid: 跳转到具体企业页面的参数
			bid: 具体企业页面URL中的参数
			name: 企业名称
			type: 企业类型
			date: 成立日期
			address: 地址
			person: 法人代表
			status: 存续状态
			regCap: 注册资本
			scope: 经营范围
	'''
	js=re_get_js.findall(html)[1]
	data=re_resultList.search(js)
	if not data:
		return
	compant_list=json.loads(data.group(1))
	
	retVal=[]
	for x in compant_list:
		regCap=x['regCap'].replace(',','')
		if regCap[-1]=='万':
			regCap=regCap[:-1]
		regCap=float(regCap)
		address=x['domicile'].replace('<em>','').replace('</em>','')
		
		temp_v={'pid':x['pid'],'bid':x['bid'],'name':x['titleName'],'type':x['entType'],'date':x['validityFrom'],\
				'address':address,'person':x['legalPerson'],'status':x['openStatus'],'regCap':regCap,\
				'scope':x['scope']}
		retVal.append(temp_v)
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
	data=Get_company_info('苏宁')
	print(data)