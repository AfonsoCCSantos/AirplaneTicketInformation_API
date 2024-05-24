# create secret
kubectl create secret generic secret-prod --from-literal=<key>=<value>

# check secrets
kubectl get secret secret-prod -o yaml

# secrets saved
DATABASE_VISUALIZATION_HOST: database-visualization=

# delete secrets
kubectl delete secret secret-prod