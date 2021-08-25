import os
import sys
import json
import time
from kafka import KafkaConsumer
import requests
from datetime import datetime
import argparse
import consumer

KAFKA_TOPIC    =  "test"

ES_SERVER = "elasticsearch-lb.elk.svc.cluster.local"
ES_PORT   = "80"
ES_INDEX  = "weather"
ES_TYPE   = "temperature"

POLL_INTERVAL = 5


def write_db(id, doc):
    url = "http://{}:{}/{}/{}/{}".format(ES_SERVER, ES_PORT, ES_INDEX, ES_TYPE, id)
    resp = requests.put(url, json=doc)
    if resp.status_code != 200 and resp.status_code != 201:
        print("Status code {}, write failed.".format(resp.status_code))
    else:
        print("Status code {}, write successful.".format(resp.status_code))


def consume_data(consumer, poll_interval):
        for message in consumer:
            data = message.value.decode('utf-8')
            id = message.offset
            print("topic={}, partition={}, offset={}, value={}".format(message.topic,
                                                                       message.partition,
                                                                       message.offset,
                                                                       data))
            jsondata = json.loads(data.replace("\'", "\""))
            #print("JSON data={}".format(jsondata))
            write_db(id, jsondata)
            time.sleep(poll_interval)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--topic", help="Kafka topic")
    parser.add_argument("-b", "--broker", help="Broker in the form BROKER_HOST:BROKER_PORT")
    parser.add_argument("-g", "--group", help="Consumer group")
    parser.add_argument("-i", "--interval", help="Polling interval in seconds")

    args = parser.parse_args()

    kafka_topic = KAFKA_TOPIC
    if args.topic:
        kafka_topic = args.topic


    if args.broker:
        try:
            kafka_host, kafka_port = args.broker.split(":")
        except ValueError as err:
            print("Error: bad kafka connection {}. {}".format(args.broker, err))
    else:
        try:
            kafka_host = os.environ['KAFKA_BROKER']
        except Exception as e:
            print("Error: Kafka host not set, defaulting to localhost")
            kafka_host = "localhost"
        try:
            kafka_port = os.environ['KAFKA_PORT']
        except Exception as e:
            print("Error: Kafka port not set, defaulting to envoy port " + e)
            kafka_port = "19092"
    
    consumer_group = None
    if args.group:
        consumer_group = args.group

    poll_interval = POLL_INTERVAL
    if args.interval:
        try:
            poll_interval = int(args.interval)
        except ValueError as err:
            print("WARNING. Bad interval value {}. {}. Defaulting to {}".format(args.interval, err, POLL_INTERVAL))

    print("Kafka server: {} \nKafka port: {} \nKafka topic: {} \nKafka consumer group: {}"
        .format(kafka_host, kafka_port, kafka_topic, consumer_group))

    try:
        bootstrap_server = [kafka_host + ":" + kafka_port]
        consumer = KafkaConsumer(kafka_topic, group_id=consumer_group, bootstrap_servers=bootstrap_server)
        consume_data(consumer, poll_interval)

    except KeyboardInterrupt as e:
        print("Ending...")


if __name__ == "__main__":
    main()
