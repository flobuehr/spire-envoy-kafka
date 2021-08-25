# Data exchange demo - Kafka integrated with Envoy proxy and SPIRE
This demo integrating Kafka with Envoy proxy and SPIRE shows the usage of service identities for service instances
* Broker
* Data producer
* Data consumer
* Federated data producer
to enable X.509 SVID-based mutual authentication and encryption (mTLS) between the service instances and federation between different trust domains.

## How to deploy the demo
### Prerequisites
* 1x 3-node K8s cluster (parta.org)
* 1x 1-node K8s cluster (partb.org)
* Command line connection (including kubeconfig file) to both clusters
* Federated SPIRE setup (link to repo missing!)

### Participant A deployment (parta.org)
Pull the repository, connect to K8s cluster of Participant-A and execute the following command to deploy the single domain Kafka demo

    $ kubectl create -k .
    
Kustomization takes care of creating all the artifacts in the K8s cluster including Zookeeper, Kafka, Producer and Consumer. In order to register the service identities with SPIRE, the following script needs to be executed

    $ ./create-registration-entries.sh parta.org partb.org
    
The command line parameters represent the trust domains of the federated SPIRE setup.

### Participant B deployment (partb.org)
For Participant B, only the remote producer is deployed. Connect to the K8s cluter of Participant-B and execute the following commands to deploy the federated producer.

    $ cd remote-producer/
    $ kubectl create -k .
    $ ./create-registration-entries.sh partb.org parta.org
    
## How to execute the demo
Open a CLI window, connect to the Participant-B K8s cluster, change directory to remote-producer/ and execute the following command

    $ ./jobp.sh
    
This publishes weather data to the topic GAIA-X of the Kafka broker running in the Participant-A cluster as displayed on stdout. Keep this running.

Open a separate CLI window, connect to the Participant-A K8s cluster, change directory to data-consumer/ and execute the following command

    $ ./jobc.sh
    
This reads the weather data from the Kafka broker as displayed on stdout. Stopping both scripts with Ctrl+C stops the demo.

## How does the demo work
This demo is based on the SPIRE deployment of two federated trust domains
* parta.org
* partb.org
representing two Participants of an ecosystem, i.e. GAIA-X. For details regarding SPIRE federation, please refer to the SPIRE federation tutorial https://github.com/spiffe/spire-tutorials/tree/master/docker-compose/federation and the SPIFFE/SPIRE documentation to deploy a federated architecture https://spiffe.io/docs/latest/architecture/federation/readme/.

The following figure describes the components and how they communicate with each other.
![Kafka demo setup](images/demo_setup.png?raw=true "Kafka demo setup")

## Modifying the demo configuration
The configuration can be applied to different environments

### Different SPIRE trust domains
The SPIRE integration is based on the Envoy configmaps
* kafka/envoy-configmap.yaml
* data-consumer/conf/envoy-config-map.yaml
* data-producer/conf/envoy-config-map.yaml
* remote-producer/conf/envoy-config-map.yaml

For Participant-A, replace all occurrences of parta.org with the trust domain of the SPIRE deployment in the Participant-A environment. Accordingly, for Participant-B, replace all occurrences of partb.org with the trust domain of the SPIRE deployment in the Participant-B environment.

The create-registration-entries.sh scripts must be executed with the corresponding trust domains as command line parameters.

# Contributors to this demo
* Christian Temporale, HPE
* Jayasheel Harugop, HPE
* Prakash Mirji, HPE
* Dominik Dufner, HPE
* Anne Huesges, HPE
* Florian Bühr, HPE
