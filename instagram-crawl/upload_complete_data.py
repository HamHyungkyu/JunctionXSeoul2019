import requests
import json
from tqdm import tqdm
import urllib.parse
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-k', '--keyword', type=str, required=True)
args = parser.parse_args()

MONGO_URL = 'http://106.10.50.27:5000/process'
MAP_SEARCH_URL = 'https://naveropenapi.apigw.ntruss.com/map-place/v1/search?orderBy=popularity&query='
GEO_SEARCH_URL = 'https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query='

with open('./hongdae_' + args.keyword + '.json') as f:
    metadata = json.loads(f.read())

cnt = 0
for doc in metadata['GraphImages']:
    try:
        result_doc = {}
        result_doc['category'] = args.keyword
        result_doc['timestamp'] = doc['taken_at_timestamp']
        result_doc['display_url'] = doc['display_url']
        result_doc['tags'] = doc['tags']
        result_doc['id'] = doc['id']

        text = doc['edge_media_to_caption']['edges'][0]['node']['text']
 
        doc['location']['address_json'] = json.loads(doc['location']['address_json'])

        map_headers = {"X-NCP-APIGW-API-KEY-ID": "l912l4ua42",
                   "X-NCP-APIGW-API-KEY": "0f3Sp1v5vLusl4JQhh32xZr542MwqIGuCnrAg527"}

        if doc['location']['address_json']['street_address']:
            juso = json.loads(requests.get(MAP_SEARCH_URL + 
                                 doc['location']['name'] + 
                                 '&coordinate=' + '126.922452,37.556725', headers=map_headers).text)
            juso = juso['places'][0]['road_address']
            if juso == "":
                raise IndexError

            result_doc['juso'] = juso
            result_doc['name'] = doc['location']['name']
           
            coord = json.loads(requests.get(MAP_SEARCH_URL + juso
                               + '&coordinate=' + '126.922452,37.556725', headers=map_headers).text)
            coord_x = coord['places'][0]['x']
            coord_y = coord['places'][0]['y']
            result_doc['x'] = coord_x
            result_doc['y'] = coord_y
            language = 'ko'
            result_doc['language'] = language

            headers = {'Content-Type': 'application/json'}
            requests.post(MONGO_URL, data=json.dumps(result_doc), headers=headers)

    except Exception as e:
        pass
