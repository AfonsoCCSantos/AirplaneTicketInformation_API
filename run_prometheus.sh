kubectl apply -f components.yaml
kubectl get all -n kube-system
# esperar que tudo fique running
kubectl create configmap prometheus-cm --from-file prometheus-cm.yaml
kubectl apply -f prometheus.yaml
kubectl port-forward service/prometheus-svc 8000:9090

kubectl delete -f components.yaml
kubectl delete cm prometheus-cm
kubectl delete -f prometheus.yaml