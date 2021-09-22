import requests
import pandas as pd
import json
import sys
import base64
import time

IS_PY3 = sys.version_info.major == 3
if IS_PY3:
    from urllib.request import urlopen
    from urllib.request import Request
    from urllib.error import URLError
    from urllib.parse import urlencode
    from urllib.parse import quote_plus
else:
    import urllib2
    from urllib import quote_plus
    from urllib2 import urlopen
    from urllib2 import Request
    from urllib2 import URLError
    from urllib import urlencode

API_KEY = 'zvj2mIZ13i4CUoQ4u3MFHtz4'
SECRET_KEY = 'BHwyzjk7m8BpqvlFOKD6Tz0hpiSzPGRg'
COMMENT_TAG_URL = "https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify"
TOKEN_URL = 'https://aip.baidubce.com/oauth/2.0/token'

def fetch_token():
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    if (IS_PY3):
        post_data = post_data.encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req, timeout=5)
        result_str = f.read()
    except URLError as err:
        print(err)
    if (IS_PY3):
        result_str = result_str.decode()

    result = json.loads(result_str)

    if ('access_token' in result.keys() and 'scope' in result.keys()):
        if not 'brain_all_scope' in result['scope'].split(' '):
            print ('please ensure has check the  ability')
            exit()
        return result['access_token']
    else:
        print ('please overwrite the correct API_KEY and SECRET_KEY')
        exit()

def post_url(url,comment):
    API_KEY = 'zvj2mIZ13i4CUoQ4u3MFHtz4'
    SECRET_KEY = 'BHwyzjk7m8BpqvlFOKD6Tz0hpiSzPGRg'
    body = {"text": comment}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36"}
    response = requests.post(url, data = json.dumps(body), headers = headers)
    response = response.json()
    #print(response)
    data = {"log_id":response["log_id"],
            "text":response["text"],
            "sentiment":response["items"][0]["sentiment"],
            "positive_prob":response["items"][0]["positive_prob"],
            "negative_prob":response["items"][0]["negative_prob"],
            "confidence":response["items"][0]["confidence"]}
    time.sleep(1)
    return data

if __name__ == "__main__":
    file_path = "极端评论数据.xlsx"
    df = pd.DataFrame(columns=["log_id","text","sentiment","positive_prob","negative_prob","confidence"])
    token = fetch_token()
    url = COMMENT_TAG_URL + "?charset=UTF-8&access_token=" + token
    a = pd.read_excel(file_path)
    for i in range(len(a)):
        comment = a.loc[i,"评论"] 
        data = post_url(url,comment)
        print(data)
        df = df.append(data,ignore_index=True)
        df.to_excel("情感分析结果.xlsx")