import requests
import re
def send_request():
    headers = headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        'Cookie': '_uab_collina=159678916887533768255393; JSESSIONID=21EE7FF8A85068502D212C7C1B267636; BIGipServerotn=1139802634.24610.0000; RAIL_EXPIRATION=1597092329089; RAIL_DEVICEID=I1dDo6IWRkLe8N0UCAm7-kBhC02clA2kM6fmg9n2-gvelMW5c_oTgb5bHwUwoH9hH1AXmL9CeBhmIms8mv9a5_a6BsViywDB8ICSt1oIL8zg8MWqmvtPJf4xxDhBr_9x8bglHbZ5Xx1nfqGTI10knzerugMo5icI; BIGipServerpool_passport=233636362.50215.0000; route=6f50b51faa11b987e576cdb301e545c4; _jc_save_fromDate=2020-08-07; _jc_save_toDate=2020-08-07; _jc_save_wfdc_flag=dc; _jc_save_fromStation=%u5317%u4EAC%2CBJP; _jc_save_toStation=%u5929%u6D25%2CTJP'}#创建头部信息
    url='https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc&fs=北京,BJP&ts=上海,SHH&date=2021-08-15&flag=N,N,Y'
    #设置编码格式。防止乱码
    resp=requests.get(url,headers=headers)
    resp.encoding='utf-8'
    return resp.text

#解析数据
#{}是字典。根据key获取值。
def parse_json(resp,city):
    import json
    json_ticket=resp.json()#将相应的数据转换为json
    data_list=json_ticket['data']['result']#得到车次的列表
    lst=[]#列表
    for item in data_list:
        #遍历车次信息进行分割
        d=item.split('|')
        lst.append([d[3],city[d[6]],city[d[7]],d[31],d[30],d[13]])
    return lst
'''
d[3]车次
d[6]查询起始站
d[7]查询到达站
d[31]一等座
d[30]表示二等座
d[13]表示出行时间'''
#获得station_name的信息
def get_city():
    url='https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9151'
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}
    resp=requests.get(url,headers=headers)
    resp.encoding='utf-8'
    #进行数据的提取(只要一部分)
    stations=re.findall('([\u4e00-\u9fa5]+)\|([A-Z]+)',resp.text)
    #将列表进行转换为字典
    stations_data=dict(stations)
    #key与value进行互换
    station_d={}#空字典。用于完成上述操作
    for item in stations_data:
        station_d[stations_data[item]]=item
    #print(station_d)
    return station_d

def start():
    #lst=parse_json(send_request(),get_city())
    print(send_request())
    #进行数据的筛选(得到有效的数据)
    for i in lst:
        if i[3]!='无' and i[3]!='':
            print(i)


if __name__=='__main__':
    start() #开始