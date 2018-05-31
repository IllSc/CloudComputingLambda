import json
from elasticsearch import Elasticsearch, RequestsHttpConnection
from elasticsearch_dsl import Search


esendpoint = 'search-cloud-computing-project-upc-uq5b7q3o57i5xaez54rlfluabu.eu-central-1.es.amazonaws.com'

def train_stations():
    return ['London Waterloo','London Victoria','London Liverpool Street','London Bridge','London Euston','Birmingham New Street','Stratford','London Paddington','London Kings Cross','London St Pancras']
def elastic_search():
    # es = Elasticsearch(hosts=[{'host': 'localhost', 'port': 9200}])
    

    es = Elasticsearch(
            hosts=[{'host': esendpoint, 'port': 443}],
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection
        )
    return es

def main(event, context):
    es = elastic_search()
    stations = train_stations()
    indexed_stations = {k: v for v, k in enumerate(stations)}

    results = []

    for origin in stations:
        temp_result = []
        for destination in stations:
            count = Search(using=es, index="train_departure").filter("range",timestamp={"gt":"now-2d/d","lt":"now/d"}).filter("match", destination_name=destination).query("match", origin_name=origin).count()
            temp_result = temp_result + [count]
            pass
        results = results + [temp_result]           
    

    print(results)
    

    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(results)
    }

    return response