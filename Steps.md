# Steps

[Parallel processing work queue](https://kubernetes.io/docs/tasks/job/fine-parallel-processing-work-queue/)

[TODO](https://medium.com/faun/35-advanced-tutorials-to-learn-kubernetes-dae5695b1f18)

## Step 1 - Build and Push Image

``` bash
./buildandpush.sh
```

## Step 2 - Create Redis pod and service

``` bash
kubectl apply -f k8s/redis-pod.yaml
kubectl apply -f k8s/redis-service.yaml
```

## Step 3 - Push to queue

``` bash
kubectl exec -it pod/redis-master -- /bin/bash
redis-cli -h redis
rpush job2 "apple" "banana" "cherry" "date" "fig" "grape" "lemon" "melon" "orange"
lrange job2 0 -1

OR 

local/push_to_queue.py 10 and local/pull_from_queue_worker.py
```

## Step 4 - Apply Job

``` bash
kubectl apply -f k8s/job.yaml
kgpo
kgaowide

kubectl describe jobs/job-wq-2
kubectl logs jobs/job-wq-2
```

## Step 5 - Cleanup

``` bash
kubectl delete -f k8s
```

### TODO

* Namespace
* ClusterIP with Ingress controller
* Integration with Prometheus + Grafana + Thanos
* Helm chart
* Skaffold
* Ambassador API gateway
* Run on EKS with EKSCTL
* Istio / Service mesh
* Patterns (https://github.com/k8spatterns/examples)