# -*- coding: utf-8 -*-

import requests
import urllib.parse
import json

headers = {"X-NCP-APIGW-API-KEY-ID": "l912l4ua42",
               "X-NCP-APIGW-API-KEY": "0f3Sp1v5vLusl4JQhh32xZr542MwqIGuCnrAg527",
               "Content-Type": "application/json"}

ROM_URL = 'https://naveropenapi.apigw.ntruss.com/krdict/v1/romanization?query='
NMT_URL = 'https://naveropenapi.apigw.ntruss.com/nmt/v1/translation'

data = {
         "source": "ko",
         "target": "en",
         "text": "경기도 용인시 마북로 55-8"
       }

print(requests.post(NMT_URL, headers=headers, data=json.dumps(data)).text)
