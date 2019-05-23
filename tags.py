import pandas as pd
import requests
import json

URL = 'http://106.10.50.27:5000/pin'

metadata = pd.read_csv('processed_data_pub_filtered.csv')
name = metadata['name'].values.tolist()
tags = metadata['tags'].values.tolist()

for i, tag in enumerate(tags):
    tags[i] = tag.replace("[", '')

for i, tag in enumerate(tags):
    tags[i] = tag.replace("]", '')

for i, tag in enumerate(tags):
    tags[i] = tag.replace("'", '')

for i, tag in enumerate(tags):
    tags[i] = tag.replace('"', '')

for i, tag in enumerate(tags):
    tags[i] = tag.replace(",", ' ')

result = {}

for _name, tag in zip(name, tags):
    try:
        for i in tag.split(' '):
            result[_name].append(i)
            
    except KeyError as e:
        result[_name] = []
        for i in tag.split(' '):
            result[_name].append(i)

name = list(set(name))
for index, _name in enumerate(name):
    counts = dict()
    for i in result[_name]:
        if i != '':
            counts[i] = counts.get(i, 0) + 1

    result[_name] = counts
print(name)
headers = {'Content-Type': 'application/json'}
for _name in name:
    data = {'name': _name, 'tags': result[_name]}
    print(data)
    requests.put(URL, headers=headers, data=json.dumps(data))
