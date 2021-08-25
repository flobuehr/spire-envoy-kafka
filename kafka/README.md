## Kafka config

Deployed kafka cluster including Zookeeper using below docs. 1 broker is deployed and the Envoy and SPIRE integration has only been tested with 1 broker. Multiple brokers require corresponding Envoy port, listener and Kafka Advertised Listener configuration, which is not part of this demo.

https://docs.bitnami.com/tutorials/deploy-scalable-kafka-zookeeper-cluster-kubernetes/

### Demo executable
The kafka broker is automatically started up with its Envoy sidecar in the kafka-0 pod. The relevant Kafka configuration can be found in the kafka-statefulset.yaml-file.

The Envoy proxy is configured with the following listening addresses and corresponding SPIFFE IDs.

          ...
          # open plaintext port w/o SPIRE integration
          socket_address:
            address: 0.0.0.0 # Host that Kafka clients should connect to.
            port_value: 9003  # Port that Kafka clients should connect to.
          ...
          # mTLS with spiffe://parta.org/kafka-demo/remote-broker federated with domain partb.org
          socket_address:
            address: 0.0.0.0 # Host that Kafka clients should connect to.
            port_value: 9002  # Port that Kafka clients should connect to.
          ...
          # mTLS with spiffe://parta.org/kafka-demo/broker no federated
          socket_address:
            address: 0.0.0.0 # Host that Kafka clients should connect to.
            port_value: 9001  # Port that Kafka clients should connect to.
          ...

Port 9003 is only exposed for test purpose, the demo only uses the SPIRE secured ports 9001 for internal parta.org publisher and subscriber and 9002 for the federated partb.org publisher.

### Playground
Changing the mutual authentication configuration in Envoy is a simple test to take away access from the publishers.

    $ ./disablepubac.sh
    
The script deploys an Envoy configuration taking away the mutual authentication of the publisher SPIFFE IDs. Demo publishing is not possible after the broker has been restartet.

    $ ./enablepubac.sh
    
This script in return deploys the original Envoy configuration to enable access of the publisher SPIFFE IDs again.
