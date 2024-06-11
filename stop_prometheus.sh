kubectl delete -f grafana.yaml
kubectl delete -f prometheus.yaml
kubectl delete cm prometheus-cm
kubectl delete -f components.yaml