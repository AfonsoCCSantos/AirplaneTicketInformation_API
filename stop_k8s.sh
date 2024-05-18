#!/bin/bash

kubectl delete -f ingress.yaml
kubectl delete -f kubernetes.yaml
kubectl delete -f prometheus.yaml
kubectl delete -f autoscaler.yaml
kubectl delete configmap prometheus-cm