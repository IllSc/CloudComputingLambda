## Steps

1. Create the Geo mapping for the index
Run the project.json mapping file: curl -XPUT https://f5674895dbb05f050cee8df674984a56.eu-west-1.aws.found.io:9243/naptan_allstops -H 'Content-Type: application/json' -d @project.json
Here, the ElasticSearch host needs to be changed

2. Update and run the Logstash config file
2.1 Update the Absolute Local Path of the csv file to be uploaded
2.2 Update the Elasticsearch Host
2.3 Run: bin\logstash -f "logstash-csv.conf"
