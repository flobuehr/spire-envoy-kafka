import sys
import os
import json
import time
import requests
import argparse
from kafka import KafkaProducer
from datetime import datetime


OPEN_WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"
APP_ID = "26fc205f8377580109c135b68836bfa6"
OPEN_WEATHER_LOC = "London"

KAFKA_TOPIC = "test"
POLL_INTERVAL = 2

def get_weather_data(location, app_id, units, debug=False):

    PARAMS = {'q': location, 'appid': app_id, 'units': units}

    # send get request to OW API
    resp = requests.get(url=OPEN_WEATHER_URL, params=PARAMS)

    data = resp.json()
    if debug:
        print("Receiving data= {}".format(data))

    weather = data['weather'][0]['main']
    weather_des = data['weather'][0]['description']
    temp = data['main']['temp']
    temp_min = data['main']['temp_min']
    temp_max = data['main']['temp_max']
    pressure = data['main']['pressure']
    ts = data['dt']
    timestamp = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%dT%H:%M:%SZ')

    w_data = { 'weather': weather,
               'weather_des': weather_des,
               'timestamp': timestamp,
               'temperature': {'cur': temp, 'min': temp_min, 'max': temp_max},
               'pressure': pressure }

    return w_data


def publish_data(producer, topic, data):
    producer.send(topic, str(data).encode())


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--topic", help="Kafka topic")
    parser.add_argument("-b", "--broker", help="Bootstrap broker in the form BROKER_HOST:BROKER_PORT")
    parser.add_argument("-n", "--num", help="Number of messages")
    parser.add_argument("-i", "--interval", help="Interval between messages in seconds")

    args = parser.parse_args()

    kafka_topic = KAFKA_TOPIC
    if args.topic:
        kafka_topic = args.topic

    if args.broker:
        try:
            kafka_broker = args.broker
        except ValueError as err:
            print("Error: bad kafka connection {}. {}".format(args.broker, err))
    else:
        try:
            kafka_broker = os.environ['KAFKA_BROKER']
        except KeyError:
            print("Error: Kafka bootstrap broker not set, defaulting to localhost:19092")
            kafka_broker = "localhost:19092"

    poll_interval = POLL_INTERVAL
    if args.interval:
        try:
            poll_interval = int(args.interval)
        except ValueError as err:
            print("WARNING. Bad interval value {}. {}. Defaulting to {}".format(args.interval, err, POLL_INTERVAL))

    num_mess = 1e6
    if args.num:
        try:
            num_mess = int(args.num)
        except ValueError as err:
            print("WARNING. Bad message number {}. {}.".format(args.num, err))

    print("Kafka bootstrap broker: {} \nKafka topic: {}\n".format(kafka_broker, kafka_topic))

    try:
        producer = KafkaProducer(bootstrap_servers=kafka_broker)

        c = 0
        while c < num_mess:
            w_data = get_weather_data(OPEN_WEATHER_LOC, APP_ID, "metric", debug=True)
            print("[{}] Publishing data: {}".format(c+1, w_data))
            publish_data(producer, kafka_topic, w_data)
            time.sleep(poll_interval)
            c += 1

    except KeyboardInterrupt:
        print("Closing...")

    except Exception as e:
        print("Kafka error: {}".format(e))

if __name__ == "__main__":
        main()


