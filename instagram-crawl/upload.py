import pandas as pd
import requests
import json
import argparse

MONGO_URL = 'http://106.10.50.27:5000/'

metadata = pd.read_csv('processed_data_pub_filtered.csv', delimiter=',')

name = metadata['name'].values.tolist()
x = metadata['x'].values.tolist()
y = metadata['y'].values.tolist()
juso = metadata['juso'].values.tolist()
tags = metadata['tags'].values.tolist()
display_url = metadata['display_url'].values.tolist()
instagram_id = metadata['id'].values.tolist()

headers = {"Content-Type": "application/json"}

n=0
for _name, _x, _y, _juso, _tags, _display_url, _instagram_id in zip(name, x, y, juso, tags, display_url, instagram_id):
    print(_tags)
    print(requests.post(MONGO_URL, headers=headers, 
                  data=json.dumps({
                           "name": _name,
                           "x": _x,
                           "y": _y,
                           "addr": _juso,
                           "tags": json.loads(_tags),
                           "display_url": _display_url,
                           "instagram_id": _instagram_id
                       })))
