#!/usr/bin/env python
import sys
import os
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
print (sys.path)

import time
import redis
import random
import json
from pysleep.rediswq import RedisWQ
from pysleep.task import Task


no_of_tasks = int(sys.argv[1])
# myhost = os.getenv("MY_DOCKER_HOST")
myhost = 'localhost'

host="redis"


# Uncomment next two lines if you do not have Kube-DNS working.
# import os
# host = os.getenv("REDIS_SERVICE_HOST")

q = RedisWQ(name="job2", host=myhost, port="6379")
print("Worker with sessionID: " +  q.sessionID())
print("Initial queue state: empty=" + str(q.empty()))
for task_no in range(no_of_tasks):
    sleeptime = random.randint(5,20)
    task = Task(task_name='TASK_'+str(task_no+1), sleep_time=sleeptime)
    print('Prepare to push')
    j = json.dumps(task.__dict__)
    q.put(j)
    print(j)
    print(f'Pushed task {task.task_name} with sleep time {task.sleep_time} seconds')
print(f"Pushed {no_of_tasks} to queue")
