import csv
import requests
import time

def Request_function(location,key,picture_name,heading):
    url = "http://api.map.baidu.com/panorama/v2"
    location = location[0] + "," + location[1]
    picture_name = picture_name + "[" + heading + "]"  + ".bmp"
    keywords = {"ak": key, "width": "480", "height": "320", "location": location,
                "coordtype": "wgs84ll", "fov": "90","heading":heading}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36"}
    a = requests.get(url, params=keywords, headers=headers)
    if a.status_code == 200:
        open(picture_name, 'wb').write(a.content)


def Run_function(pos_reader,number,Key_number):
    for a in pos_reader[1:]:
        lng = a[1]
        lat = a[2]
        name = a[0] 
        tq = len(pos_reader) - 1
        position = [str(lng),str(lat)]
        if number % 25 == 0:
            Key_number = Key_number + 1
        key_result = key[Key_number]
        picture_name = str(name)
        number = number+1
        heading = ["0","90","180","270"]
        try:
            Request_function(position,key_result,picture_name,heading[0])
            Request_function(position,key_result,picture_name,heading[1])
            Request_function(position,key_result,picture_name,heading[2])
            Request_function(position,key_result,picture_name,heading[3])
            time.sleep(1)
            print("开始下载编号为{}的街景，目前为第{}个点，项目进展至{:.2%}".format(name,number-1,(number-1)/tq))
        except:
            print("编号为{}的街景下载失败".format(name))


if __name__ == "__main__":
    """配置区域"""
    Key_file = "key.csv"
    location_file = "location.csv"
    """运行区域"""
    key = []
    number = 1
    Key_number = 1
    key = list(csv.reader(open(Key_file, encoding='UTF-8')))
    pos_reader = list(csv.reader(open(location_file, encoding='UTF-8')))
    Run_function(pos_reader,number,Key_number)


