#! /usr/bin/env bash

producerpod=`kubectl get pods | grep ^data-producer | awk '{print $1}'`

kubectl exec -it ${producerpod} -c data-producer -- python publisher.py -t gaiax -b localhost:19092 -i 5
