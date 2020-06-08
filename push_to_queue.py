#!/usr/bin/env python

import sys
import time
import redis
import rediswq
import random
import json
from task import Task


no_of_tasks = int(sys.argv[1])
host="redis"


# Uncomment next two lines if you do not have Kube-DNS working.
# import os
# host = os.getenv("REDIS_SERVICE_HOST")

q = rediswq.RedisWQ(name="job2", host="192.168.1.176", port="30379")
# print("Worker with sessionID: " +  q.sessionID())
# print("Initial queue state: empty=" + str(q.empty()))
for task_no in range(no_of_tasks):
    sleeptime = random.randint(10,30)
    task = Task(task_name=f'TASK{task_no}', sleep_time=sleeptime)
    print('Prepare to push')
    j = json.dumps(task.__dict__)
    q.put(j)
    print(j)
    print(f'Pushed task {task.task_name} with sleep time {task.sleep_time} seconds')
print(f"Pushed {no_of_tasks} to queue")
