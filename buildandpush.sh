cd pysleep
docker build -t job-wq-2 .
docker tag job-wq-2 rahulh77/job-wq-2
docker push rahulh77/job-wq-2