# PySleep

[PySleep](https://kubernetes.io/docs/tasks/job/fine-parallel-processing-work-queue/)

## Step 1

``` bash
./buildandpush.sh
```

## Step 2

``` bash
kubectl apply -f k8s/redis-pod.yaml
kubectl apply -f k8s/redis-service.yaml
```

## Step 3

``` bash
kubectl exec -it pod/redis-master -- /bin/bash
redis-cli -h redis
rpush job2 "apple"
rpush job2 "banana"
rpush job2 "cherry"
rpush job2 "date"
rpush job2 "fig"
rpush job2 "grape"
rpush job2 "lemon"
rpush job2 "melon"
rpush job2 "orange"
lrange job2 0 -1
```

## Step 4

``` bash
kubectl apply -f k8s/job.yaml
kubectl describe jobs/job-wq-2
kubectl logs jobs/job-wq-2
```
