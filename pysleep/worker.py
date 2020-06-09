#!/usr/bin/env python

import time
import rediswq
import sys
import time
import redis
import rediswq
import random
import json
from task import Task

q = rediswq.RedisWQ(name="job2", host="redis")
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
