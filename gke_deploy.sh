#minikube start
gcloud auth login
gcloud config set project disco-parsec-415719
gcloud container clusters create-auto cn19-cluster --region=europe-west4 #nmbr nodes, tipo de maquina
gcloud container clusters get-credentials cn19-cluster --region=europe-west4
kubectl config current-context

kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.6.4/deploy/static/provider/cloud/deploy.yaml
kubectl apply -f ingress.yaml
kubectl apply -f kubernetes.yaml
kubectl apply -f autoscaler.yaml
#kubectl port-forward --namespace=ingress-nginx service/ingress-nginx-controller 8080:80

kubectl get ingress # obter ip
gcloud container clusters delete cn19-cluster --region=europe-west4