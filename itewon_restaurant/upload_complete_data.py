import requests
import json
from tqdm import tqdm

with open('./itewon_restaurant.json') as f:
    metadata = json.loads(f.read())

cnt = 0
for doc in metadata['GraphImages']:
    try:
        result_doc = {}
        result_doc['timestamp'] = doc['taken_at_timestamp']
        result_doc['display_url'] = doc['display_url']
        result_doc['tags'] = doc['tags']
        result_doc['id'] = doc['id']
   
        if doc['location'] is not None:
            print(doc['location'])
            cnt += 1

    except KeyError as e:
        continue
