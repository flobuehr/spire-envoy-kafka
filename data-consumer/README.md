## Kafka consumer

The Kafka consumer is a python service that reads messages from the Kafka broker
on a given topic. 

### Demo executable
The script executes the python script in the data consumer container acting as a Kafka subscriber and communicating according to the configured ports with the broker.

    $ ./jobc.sh
    
The default target used for communication of the subscriber script is localhost:19092, which is the Envoy proxy sidecar of the data consumer pod, and the configured Kafka topic is GAIA-X.

### How to execute the python script

Find the data-consumer pod

    $ kubectl get pod | grep data-consumer
    
Connect to the data-consumer container inside the pod (being envoy the other one):

    $ kubectl exec -it <consumer pod> -c data-consumer /bin/bash
    
Inside the container, run the publisher program to publish messages to a Kafka broker and a given subject:

    $ python consumer.py [-h] [-t TOPIC] [-b BROKER] [-i INTERVAL]
    
Where the optional arguments are:
- ````TOPIC````: Kafka topic 
- ````BROKER````: Kafka broker in the form {HOST}:{PORT}. The default uses Envoy, 
so {HOST}=localhost and {PORT}=19092
- ````INTERVAL````: Interval between messages in seconds (default 2)

Example

    $ python consumer.py -t weather
