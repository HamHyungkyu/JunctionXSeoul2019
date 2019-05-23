import json
import requests
import pandas as pd

URL = 'http://106.10.50.27:5000/pin'

metadata = pd.read_csv('processed_data_pub_PIN.csv')
name = metadata['name'].values.tolist()
juso = metadata['juso'].values.tolist()
x = metadata['x'].values.tolist()
y = metadata['y'].values.tolist()
num = metadata['num'].values.tolist()

for _name, _juso, _x, _y, _num in zip(name, juso, x, y, num):
    doc = {
              "name": _name,
              "location": {
                  "lat": _y,
                  "lng": _x
              },
              "addr": _juso,
              "post": {
                  "num": _num,
                  "tags": []
              }
          }
    headers = {'Content-Type': 'application/json'}
    print(requests.post(URL, headers=headers, data=json.dumps(doc)))


