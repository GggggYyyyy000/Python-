import pandas as pd
import requests
import json

df = pd.read_csv("/Users/creative/Documents/python/Test files area/100OD(1).csv")

url = 'https://restapi.amap.com/v3/direction/driving?parameters'
key = "376e811e3c5fe9355aada73ad7473a36"

def get_data():
    zd = []
    for i in range(0,1):
        ox_df = df.loc[i,'ox']
        oy_df = df.loc[i,'oy']
        dx_df = df.loc[i,'dx']
        dy_df = df.loc[i,'dy']
        ox_oy = str(ox_df) + ',' + str(oy_df)
        dx_dy = str(dx_df) + ',' + str(dy_df)
        keywords = { "key": key , 'origin':ox_oy , 'destination':dx_dy , 'extensions':'base'}
        r = requests.get(url,params=keywords,timeout=10)
        print(r.url)
        
        if r.status_code == 200:
        
            m = r.text
            data = json.loads(m)
            
            js = {}
            #爬取坐标、距离、时间
            js['origin'] = data['route']['origin']
            js['destination'] = data['route']['destination']
            js['distance'] = data['route']['paths'][0]['distance']
            js['duration'] = data['route']['paths'][0]['duration']
            
            lst = []
            cs = {}
            #爬取具体路径坐标，提取路径坐标合到一个列表中  
            cs['a'] = data['route']['paths'][0]['steps']
            for x in range(len(cs['a'])): 
                cs['polyline'] = cs['a'][x]['polyline']
                for m in cs['polyline'].split(';') :
                    lst.append(m)  #有重复坐标           
                    #yield lst

            b = list(set(lst))  #利用集合去掉重复值
            b.sort(key = lst.index)  #保证重新生成的列表序列不变
            
            for n in range(len(b)):
                zzz = {'id':i+1,'number':n+1,'x':b[n].split(',')[0],'y' :b[n].split(',')[1]}
                zd.append(zzz)
    return zd
            
            
dt = get_data()
s = pd.DataFrame(dt)
#s.to_csv('D:\\postgraduate\\python_holiday homework\\1\\zb_100OD.csv',index = False,mode='a')
