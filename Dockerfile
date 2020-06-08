FROM python
RUN pip install redis
COPY ./task.py /task.py
COPY ./worker.py /worker.py
COPY ./rediswq.py /rediswq.py

CMD  python worker.py
