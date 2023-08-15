# 
FROM python:3.11

# 
WORKDIR /app

# 
COPY requirements.txt requirements.txt

#
RUN apt-get update
RUN apt-get install -y cron
RUN pip install --no-cache-dir --upgrade -r requirements.txt
