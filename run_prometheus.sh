kubectl apply -f components.yaml
# wait for components to run
#kubectl get all -n kube-system
kubectl wait --namespace kube-system \
 --for=condition=ready pod \
 --selector=k8s-app=metrics-server \
 --timeout=180s

kubectl create configmap prometheus-cm --from-file prometheus-cm.yaml
kubectl apply -f prometheus.yaml

# wait for prometheus to run
kubectl wait --namespace default \
  --for=condition=available deployment/prometheus-deployment \
  --timeout=180s

kubectl port-forward service/prometheus-svc 8000:9090

