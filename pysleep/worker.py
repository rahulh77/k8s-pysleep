#!/usr/bin/env python

import os
import time
import rediswq
import sys
import time
import redis
import rediswq
import random
import json
from task import Task
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway, pushadd_to_gateway


q = rediswq.RedisWQ(name="job2", host="redis")
print("Worker with sessionID: " +  q.sessionID())
print("Initial queue state: empty=" + str(q.empty()))

# PUSHGATEWAY_URL = 'localhost:9091'
PUSHGATEWAY_URL = 'monitoring-pushgateway-prometheus-pushgateway.monitoring.svc.cluster.local:9091'
REGISTRY = CollectorRegistry()
JOB='my_pysleep_job'
INSTANCE=os.environ.get('INSTANCE_NAME', 'NO_INSTANCE')

g = Gauge(name='pysleep_requests_gauge', documentation='Description of gauge', labelnames=['task_no', 'status', 'sleep_time', 'instance'], registry=REGISTRY)
while not q.empty():
  item = q.lease(lease_secs=10, block=True, timeout=2) 
  if item is not None:
    itemstr = item.decode("utf-8")
    print("Task: ", itemstr)
    j = json.loads(itemstr)
    task = Task(**j)
    print("Working on " + task.task_name)
    
    # Task Start
    g.labels(task.task_name, 'started', task.sleep_time, INSTANCE).set(1)
    pushadd_to_gateway(PUSHGATEWAY_URL, job=JOB, registry=REGISTRY)
    time.sleep(task.sleep_time) # Put your actual work here instead of sleep.
    # Task End
    g.labels(task.task_name, 'completed', task.sleep_time, INSTANCE).set(2)
    pushadd_to_gateway(PUSHGATEWAY_URL, job=JOB, registry=REGISTRY)
    print('Pushed to pushgateway: ', task.task_name)

    q.complete(item)
  else:
    print("Waiting for work")
print("Queue empty, exiting")
