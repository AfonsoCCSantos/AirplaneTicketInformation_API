kubectl apply -f components.yaml
# wait for components to run
#kubectl get all -n kube-system
kubectl wait --namespace kube-system \
 --for=condition=ready pod \
 --selector=k8s-app=metrics-server \
 --timeout=300s

kubectl create configmap prometheus-cm --from-file prometheus-cm.yaml
kubectl apply -f prometheus.yaml

# wait for prometheus to run
kubectl wait --namespace default \
  --for=condition=ready pod \
  --selector=app=prometheus \
  --timeout=300s

kubectl apply -f grafana.yaml
kubectl wait --namespace default \
  --for=condition=ready pod \
  --selector=app=grafana,purpose=monitoring-demo \
  --timeout=300s
kubectl port-forward service/grafana-svc 8000:3000


