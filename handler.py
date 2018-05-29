import json
import boto3
import logging
import random
import io
import hashlib
import pprint
from datetime import datetime

log = logging.getLogger()
log.setLevel(logging.DEBUG)

from botocore.vendored import requests
from elasticsearch import Elasticsearch, RequestsHttpConnection
from boto3.dynamodb.conditions import Key
from random import randint


esendpoint = 'search-cloud-computing-project-upc-uq5b7q3o57i5xaez54rlfluabu.eu-central-1.es.amazonaws.com'

def train_stations():
    return ['WAT','VIC','LST','LBG','EUS','BHM','SRA','PAD','KGX','STP']

def api_credentials():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table("credentials")

    response = table.query(
    KeyConditionExpression=Key('id').eq(randint(1, 4))
    )
    items = response['Items']
    entry = items[0]
    return (entry['app_id'],entry['app_key'])

def build_response(app_id,app_key,station):
    url = "https://transportapi.com/v3/uk/train/station/{:s}/live.json".format(station)
    querystring = {"app_id":app_id,"app_key":app_key,"darwin":"false","train_status":"passenger"}
    headers = {}
    return requests.request("GET", url, headers=headers, params=querystring)

def elastic_search():
    # es = Elasticsearch(hosts=[{'host': 'localhost', 'port': 9200}])
    

    es = Elasticsearch(
            hosts=[{'host': esendpoint, 'port': 443}],
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection
        )
    return es


def hello(event, context):
    es = elastic_search()
    stations = train_stations()
    for station in stations:
        (app_id,app_key) = api_credentials()
        response = build_response(app_id,app_key,station)

        json_response = response.json()

        departures = json_response['departures']['all']
        for departure in departures:
            departure['timestamp'] = datetime.now().isoformat()
            document_index = hashlib.md5(json.dumps(departure, sort_keys=True).encode('utf-8')).hexdigest()
            es.index(index='train_departure', doc_type='travel', id=document_index, body=departure)
            pass
        pass

    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """
