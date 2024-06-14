if [ -z "$1" ]; then
    echo "No parameter provided."
    exit 1
fi

if [ $1 = "alex" ]; then
    PROJECT_ID="disco-parsec-415719"
elif [ $1 = "afonso" ]; then
    PROJECT_ID="fcul123-415719"
elif [ $1 = "raquel" ]; then
    PROJECT_ID="fcul-2024-cn"
elif [ $1 = "tomas" ]; then
    PROJECT_ID="cloudcomputing111"
elif [ $1 = "miguel" ]; then
    PROJECT_ID="cloudcomputing-415913"
fi
echo $PROJECT_ID
gcloud auth login
gcloud config set project $PROJECT_ID

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