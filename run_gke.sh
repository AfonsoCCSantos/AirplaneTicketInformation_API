gcloud auth login
gcloud config set project disco-parsec-415719

# default MACHINE_TYPE: e2-medium
# gcloud container clusters create-auto cn19-cluster --region=europe-west4 #nmbr nodes, tipo de maquina


gcloud container clusters create cn19-cluster --region=europe-west4 \
    --node-locations europe-west4-a \
    --num-nodes=5 \
    --machine-type=custom-1-2048 # com 5 nodes 1 vcpu e 2 de mem per node


gcloud container clusters get-credentials cn19-cluster --region=europe-west4 

kubectl config current-context

./run_k8s.sh
#kubectl port-forward --namespace=ingress-nginx service/ingress-nginx-controller 8080:80
#disco-parsec-415719
#kubectl get ingress # obter ip