# How to rollback/rollout

### Check history of updates
kubectl rollout history deployment/<name>

kubectl rollout undo deployment/<name> --to-revision=<revision-number>