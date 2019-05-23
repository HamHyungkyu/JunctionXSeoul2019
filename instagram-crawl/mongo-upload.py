import pymongo
from pymongo import MongoClient
import urllib.parse
import json
from bson import ObjectId
from flask import Flask, request
from flask_restful import Resource, Api
from flask_restful import reqparse
from flask_cors import CORS

import numpy as np
import requests

GOOGLE_URL = 'https://maps.googleapis.com/maps/api/place/details/json?placeid='
KEY = '&key=AIzaSyCRfZVReuq7z6dmpTsjJcjTb1SOzHVsaN8'

app = Flask(__name__)
cors = CORS(app, resourcecs={r"/*": {"origins": "*"}})
api = Api(app)

username = urllib.parse.quote_plus('admin')
password = urllib.parse.quote_plus('junctionx')

class UploadCompleteData(Resource):
    mongoClient = MongoClient('mongodb://%s:%s@127.0.0.1' % (username, password))
    junctionDb = mongoClient['junctionx']
    collectionCompleteData = junctionDb['complete_data']

    def post(self):
        content = request.get_json()
        self.collectionCompleteData.insert(content)

        return {"message": "success"}

class UploadProcessedData(Resource):
    mongoClient = MongoClient('mongodb://%s:%s@127.0.0.1' % (username, password))
    junctionDb = mongoClient['junctionx']
    collectionProcessedData = junctionDb['processed_data']

    def post(self):
        content = request.get_json()
        self.collectionProcessedData.insert(content)

        return {"message": "success"}

class ImageByName(Resource):
    mongoClient = MongoClient('mongodb://%s:%s@127.0.0.1' % (username, password))
    junctionDb = mongoClient['junctionx']
    collectionData = junctionDb['complete_data']
    def get(self):
        args = request.args
        docs = self.collectionData.find({"name": args['name']})

        result = []
        for doc in docs:
            del doc['_id']
            result.append({"image_url": doc['display_url'], "instagram_id": doc['instagram_id']})

        return result

class TranslateAll(Resource):
    mongoClient = MongoClient('mongodb://%s:%s@127.0.0.1' % (username, password))
    junctionDb = mongoClient['junctionx']
    collectionPins = junctionDb['pins']

    def _translate(self, text):
        NMT_URL = 'https://naveropenapi.apigw.ntruss.com/nmt/v1/translation'
        headers = {"X-NCP-APIGW-API-KEY-ID": "l912l4ua42",
               "X-NCP-APIGW-API-KEY": "0f3Sp1v5vLusl4JQhh32xZr542MwqIGuCnrAg527",
               "Content-Type": "application/json"}

        data = {
           "source": "ko",
           "target": "en",
           "text": text
        }
        result = json.loads(requests.post(NMT_URL, headers=headers, data=json.dumps(data)).text)
        return result['message']['result']['translatedText']

    def put(self):
        docs = self.collectionPins.find({})
        for doc in docs:
            new_doc = {}
            new_doc['addr'] = self._translate(doc['addr'])
            new_doc['name'] = doc['name']
            new_doc['location'] = doc['location']
            new_doc['post'] = {"num": doc['post']['num'], 'tags': {}}
            try:
                for i, v in doc['post']['tags'].items():
                    new_doc['post']['tags'][self._translate(i)] = v
            except:
                pass
            
            self.collectionPins.update({"name": new_doc['name']}, new_doc)

        return {"message": "success"}

class Pins(Resource):
    mongoClient = MongoClient('mongodb://%s:%s@127.0.0.1' % (username, password))
    junctionDb = mongoClient['junctionx']
    collectionPins = junctionDb['pins']
    collectionData = junctionDb['complete_data']

    def get(self):
        args = request.args
        x1 = float(args['x1'])
        x2 = float(args['x2'])
        y1 = float(args['y1'])
        y2 = float(args['y2'])

        docs = self.collectionPins.find({})

        result = []
        for doc in docs:
            new_doc = doc
            del new_doc['_id']
            if x1 <= doc['location']['lng'] <= x2 and y1 <= doc['location']['lat'] <= y2:
                image_doc = self.collectionData.find({"name": doc['name']})
                new_doc['image_url'] = []
                for img in image_doc:
                    new_doc['image_url'].append(img['display_url'])

                result.append(new_doc)

        return result


    def post(self):
        content = request.get_json()
        self.collectionPins.insert(content)

        return {"message": "success"}

    def put(self):
        content = request.get_json()
        
        doc = self.collectionPins.find_one({"name": content['name']})
        print(doc)
        doc['post']['tags'] = content['tags']

        self.collectionPins.update({"name": content['name']}, doc, upsert=True)
        return {"message": "success"}

class MapApi(Resource):
    def get(self):
        args = request.args

        headers = {'Content-Type': 'application/json'}
        res = requests.get(GOOGLE_URL + args['placeid'] + KEY, headers=headers)

        return json.loads(res.text)



api.add_resource(UploadCompleteData, '/')
api.add_resource(UploadProcessedData, '/process')
api.add_resource(ImageByName, '/image')
api.add_resource(Pins, '/pin')
api.add_resource(MapApi, '/map')
api.add_resource(TranslateAll, '/translate')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
