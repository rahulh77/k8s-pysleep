# Steps

[Parallel processing work queue](https://kubernetes.io/docs/tasks/job/fine-parallel-processing-work-queue/)
[Workshop](https://github.com/juliusv/prometheus_workshop/blob/master/workshop.md)
[TODO](https://medium.com/faun/35-advanced-tutorials-to-learn-kubernetes-dae5695b1f18)

## Shortcuts

``` bash
kubens
kga
kgpo
kgns
kaf
krmf
```

## Setup Prom-Operator and Grafana

``` bash
helm repo add stable https://kubernetes-charts.storage.googleapis.com/
helm repo update
kubectl create namespace monitoring
helm install monitoring --namespace monitoring stable/prometheus-operator

or
# Edit values.yaml (ClusterIP -> LoadBalancer and default ports) and run
cd to helm chart stable prometheus
helm upgrade monitoring --namespace monitoring .
kgaowide
# Change below service from clusterip to load balancer
kubectl edit service/monitoring-prometheus-oper-prometheus
kgaowide

cd to helm chart stable grafana
helm upgrade grafana --namespace monitoring . --set persistence.enabled=false
admin/admin


http://localhost:9090/graph
http://localhost:9091/
http://localhost:9093/#/alerts


# Change below service from clusterip to load balancer
# and port from 80 to 3000
kubectl edit service/monitoring-grafana
# UI Login: localhost:3000; admin/prom-operator

helm install monitoring-pushgateway --namespace monitoring --set service.type=LoadBalancer stable/prometheus-pushgateway
```

## Step 1 - Build and Push Image

``` bash
./buildandpush.sh
```

## Step 2 - Create Redis pod and service in namespace

``` bash
kubectl apply -f k8s/00-ns-pysleep.yaml
kubectl apply -f k8s/01-redis-pod.yaml
kubectl apply -f k8s/02-redis-service.yaml
OR
ka -f k8s/00-ns-pysleep.yaml -f k8s/01-redis-pod.yaml -f k8s/02-redis-service.yaml
```

## Step 3 - Push to queue

[port forward](https://kubernetes.io/docs/tasks/access-application-cluster/port-forward-access-application-cluster/)

``` bash
kubectl exec -it pod/redis-master -- /bin/bash
redis-cli -h redis
rpush job2 "apple" "banana" "cherry" "date" "fig" "grape" "lemon" "melon" "orange"
lrange job2 0 -1

OR
# Setup kubectl proxy (To access Clusterip/port inside eks cluster)
kubectl port-forward service/redis 7000:6379
local/push_to_queue.py 10
# and local/pull_from_queue_worker.py (for local testing)
```

## Step 4 - Apply Job

``` bash
kubectl apply -f k8s/job.yaml
kgpo
kgaowide

kubens ns-pysleep
kubectl describe jobs/job-wq-2
kubectl logs jobs/job-wq-2 -f
```

## Step 5 - Cleanup

``` bash
kubectl delete -f k8s
krmf k8s

curl -X DELETE http://localhost:9091/metrics/job/job-wq-2/instance/job-wq-2-42jc8
```

### TODO

* Namespace
* kubeproxy
* Integration with Prometheus + Grafana + Thanos
* ClusterIP with Ingress controller
* Helm chart
* Skaffold
* Ambassador API gateway
* Run on EKS with EKSCTL
* Istio / Service mesh
* Patterns [k8s patterns](https://github.com/k8spatterns/examples)

* node exporter (for server level metrics - e.g. linux server metrics)
* custom exporter (for trd party (of the shelf) applications, batch processor)
* client library (for application metrics - e.g. web application metrics)
* push gateway - for short lived jobs
