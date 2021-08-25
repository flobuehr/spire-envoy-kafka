#! /usr/bin/env bash

consumerpod=`kubectl get pods | grep ^data-consumer | awk '{print $1}'`

kubectl exec -it ${consumerpod} -c data-consumer -- python consumer.py -t gaiax -b localhost:19092 -i 5
