FROM python
RUN pip install redis
COPY pysleep/task.py /task.py
COPY pysleep/worker.py /worker.py
COPY pysleep/rediswq.py /rediswq.py

CMD  python -u worker.py
