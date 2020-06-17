FROM python

WORKDIR /opt/pysleep
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY pysleep/task.py task.py
COPY pysleep/worker.py worker.py
COPY pysleep/rediswq.py rediswq.py

CMD  python -u worker.py
