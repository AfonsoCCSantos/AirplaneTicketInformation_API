#!/bin/bash

kubectl delete -f ingress.yaml
# kubectl delete -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.6.4/deploy/static/provider/cloud/deploy.yaml
kubectl delete -f kubernetes.yaml
kubectl delete -f autoscaler.yaml