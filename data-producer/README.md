## Kafka producer

The Kafka producer is a python service that fetches info from [Open Weather API](https://openweathermap.org/api) 
and publishes them to Kafka broker. It exposes a minimal set of API to control frequency and number of messages to 
publish  

### Demo executable
The script executes the python script in the data producer container acting as a Kafka publisher and communicating according to the configured ports with the broker.

    $ ./jobp.sh
    
The default target used for communication of the publisher script is localhost:19092, which is the Envoy proxy sidecar of the data consumer pod, and the configured Kafka topic is GAIA-X.

### Publish directly from inside the container
Find the data-producer pod

    $ kubectl get pod | grep data-producer
    
Connect to the data-producer container inside the pod (being envoy the other one):

    $ kubectl exec -it <producer pod> -c data-producer /bin/bash
    
Inside the container, run the publisher program to publish messages to a Kafka broker and a given subject:

    $ python publisher.py [-h] [-t TOPIC] [-b BROKER] [-n NUM] [-i INTERVAL]
    
Where the optional arguments are:
- ````TOPIC````: Kafka topic 
- ````BROKER````: Kafka broker in the form {HOST}:{PORT}. The default uses Envoy, 
so {HOST}=localhost and {PORT}=19092
- ````NUM````: Number of messages to publish (default: it keeps publishing until you press CTRL-C) 
- ````INTERVAL````: Interval between messages in seconds (default 2)

Example

    $ python publisher.py -t weather -n 10
    
### Publish using UI
This is not part of the demo setup, but included in this repository. To deploy and activate, remote the comment in the conf/kustomization.yaml-file and redo the deployment. Once the producer service is deployed and activated, proceed as follows.

Get the external service IP and port:

    > kubectl get svc publisher
    NAME        TYPE           CLUSTER-IP   EXTERNAL-IP     PORT(S)                          AGE
    publisher   LoadBalancer   10.78.6.10   34.122.54.198   19092:30764/TCP,5005:31764/TCP   5d19h

and point your browser to <EXTERNAL_IP>:<external port> (in this example: http://34.122.54.198:5005/). 
Here you can set:
- Kafka topic
- Number of messages to publish (batch size)
- Interval of time between them (in seconds)


### Publish using REST API
This is not part of the demo setup, but included in this repository. To deploy and activate, remote the comment in the conf/kustomization.yaml-file and redo the deployment. Once the producer service is deployed and activated, proceed as follows.

Get the external service IP and port (see Publish using UI).
Use whatever tool (curl, postman, etc.) to send REST commands to the following base BASE_URL:

http://<EXTERNAL_IP>:<external port>/api (e.g. http://34.122.54.198:5005/api)

To get the current configuration:
    
    GET <BASE_URL>


To publish a message on a given topic, batch size and interval, use <BASE_URL/publish and POST or PUT 
those information in JSON format, e.g.: 

    POST http://34.122.54.198:5005/api/publish
    {
        "topic": "test",
        "batch_size": 3,
        "interval": 1
    }

To set the defautl topic to a given subject:

    PUT <BASE_URL>
    {
        "topic": "test2",
    }
