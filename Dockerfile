# 
FROM python:3.11

#
COPY . /app

# 
WORKDIR /app

#
RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD alembic upgrade head;python -m uvicorn main:app --host 0.0.0.0 --port 3000