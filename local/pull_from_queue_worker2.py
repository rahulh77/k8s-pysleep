#!/usr/bin/env python

import sys
import os
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
print (sys.path)

import time
import sys
import time
import redis
from pysleep.rediswq import RedisWQ
import random
import json
from pysleep.task import Task
from prometheus_client import CollectorRegistry, Gauge, pushadd_to_gateway, push_to_gateway

# myhost= "<my_host_ip>" # "redis"
# myhost = os.getenv("MY_DOCKER_HOST")
myhost = 'localhost'


PUSHGATEWAY_URL = 'localhost:9091'
REGISTRY = CollectorRegistry()
JOB='my_pysleep_job'

INSTANCE=os.environ.get('INSTANCE_NAME', 'NO_INSTANCE')

# Host address is the host machine ip, port is the forwarded port
q = RedisWQ(name="job2", host=myhost, port="6379")
print("Worker with sessionID: " +  q.sessionID())
print("Initial queue state: empty=" + str(q.empty()))

while not q.empty():
  item = q.lease(lease_secs=10, block=True, timeout=2) 
  if item is not None:
    itemstr = item.decode("utf-8")
    print("Task: ", itemstr)
    j = json.loads(itemstr)
    task = Task(**j)
    print("Working on " + task.task_name)
    
    # Task Start
    g = Gauge(name=task.task_name, documentation='Description of gauge', labelnames=['task_no', 'status', 'sleep_time', 'instance'], registry=REGISTRY)
    # g.labels(task.task_name).set(1)
    g.labels(task_no=task.task_name, status='started', sleep_time=task.sleep_time, instance=INSTANCE).set(1)
    push_to_gateway(PUSHGATEWAY_URL, job=JOB, registry=REGISTRY)
    time.sleep(task.sleep_time) # Put your actual work here instead of sleep.
    # Task End
    # g.labels(task.task_name).set(2)
    g.labels(task_no=task.task_name, status='started', sleep_time=task.sleep_time, instance=INSTANCE).set(2)
    push_to_gateway(PUSHGATEWAY_URL, job=JOB, registry=REGISTRY)
    print('Pushed to pushgateway: ', task.task_name)

    q.complete(item)
  else:
    print("Waiting for work")
print("Queue empty, exiting")
