import requests
import time
import hashlib
import base64
import json
import yaml
import urllib

with open('配置.yaml') as f:
    配置 = yaml.load(f)
    Appid = 配置['Appid']
    Key = 配置['Key']

def 訊飛連線(type, text):
    CurTime = str(int(time.time()))
    Param = 'eyJ0eXBlIjoiZGVwZW5kZW50In0='
    md5 = hashlib.md5((Key + CurTime + Param).encode())
    res = md5.hexdigest()
    headers = {
        'X-Appid': Appid,
        'X-CurTime': CurTime,
        'X-Param': Param,
        'X-CheckSum': res,
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
    }

    body = urllib.parse.urlencode({'text': text})

    s = requests.Session()
    s.headers = headers
    res = s.post(url=f'http://ltpapi.xfyun.cn/v1/{type}', data=body)

    return json.loads(res.text)["data"]


def 分詞(text):
    return 訊飛連線('cws', text)["word"]

def 依存分析(text):
    return 訊飛連線('sdp', text)["sdp"]
