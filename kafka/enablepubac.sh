#! /usr/bin/env bash
kubectl apply -f envoy-configmap.yaml
kubectl delete pod kafka-0
sleep 10 
kubectl get pods

