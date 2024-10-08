#!/bin/bash

./create_secrets.sh
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.6.4/deploy/static/provider/cloud/deploy.yaml
# kubectl get pods --namespace=ingress-nginx
kubectl wait --namespace ingress-nginx \
 --for=condition=ready pod \
 --selector=app.kubernetes.io/component=controller \
 --timeout=300s

kubectl apply -f ingress.yaml
kubectl apply -f kubernetes.yaml
kubectl apply -f autoscaler.yaml
# kubectl port-forward --namespace=ingress-nginx service/ingress-nginx-controller 8080:80
