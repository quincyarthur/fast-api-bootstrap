# 
FROM python:3.11

# 
WORKDIR /app

# 
COPY requirements.txt requirements.txt

#
RUN apt-get update
RUN apt-get install -y cron
RUN apt-get install sudo
RUN adduser root sudo
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN sudo mkdir /var/log/remove_expired_user_accounts
RUN sudo chown -R root:root /var/log/remove_expired_user_accounts
RUN sudo supervisord -c /app/src/background_jobs/supervisord.conf
