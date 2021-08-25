#!/usr/bin/bash

LOCDOMAIN=$1
REMOTEDOMAIN=$2

kubectl exec -n spire spire-server-0 -- /opt/spire/bin/spire-server entry create -spiffeID spiffe://${LOCDOMAIN}/kafka-demo/subscriber -parentID spiffe://${LOCDOMAIN}/ns/spire/sa/spire-agent -selector k8s:ns:default -selector k8s:sa:default -selector k8s:container-name:envoy -selector k8s:pod-label:app:subscriber
kubectl exec -n spire spire-server-0 -- /opt/spire/bin/spire-server entry create -spiffeID spiffe://${LOCDOMAIN}/kafka-demo/publisher -parentID spiffe://${LOCDOMAIN}/ns/spire/sa/spire-agent -selector k8s:ns:default -selector k8s:sa:default -selector k8s:container-name:envoy -selector k8s:pod-label:app:publisher
kubectl exec -n spire spire-server-0 -- /opt/spire/bin/spire-server entry create -spiffeID spiffe://${LOCDOMAIN}/kafka-demo/broker -parentID spiffe://${LOCDOMAIN}/ns/spire/sa/spire-agent -selector k8s:ns:default -selector k8s:sa:default -selector k8s:container-name:envoy -selector k8s:pod-label:app.kubernetes.io/name:kafka
