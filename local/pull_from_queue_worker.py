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

# myhost= "<my_host_ip>" # "redis"
myhost = os.getenv("MY_DOCKER_HOST")

# Host address is the host machine ip, port is the forwarded port
q = RedisWQ(name="job2", host=myhost, port="30379")
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
    time.sleep(task.sleep_time) # Put your actual work here instead of sleep.
    q.complete(item)
  else:
    print("Waiting for work")
print("Queue empty, exiting")
