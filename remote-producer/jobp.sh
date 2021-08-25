#! /usr/bin/env bash

PORT=$1
producerpod=`kubectl get pods | grep ^data-producer | awk '{print $1}'`
if [[ PORT -gt 0 ]]; then
	kubectl exec -it ${producerpod} -c data-producer -- python publisher.py -t gaiax -b localhost:${PORT} -i 5
else
	kubectl exec -it ${producerpod} -c data-producer -- python publisher.py -t gaiax -b localhost:19092 -i 5
fi
