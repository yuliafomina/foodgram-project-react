FROM python:3.7-slim

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt --no-cache-dir

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000", "--error-logfile", "/app/logs/error.log", "--access-logfile", "/app/logs/access.log", "--capture-output", "--log-level", "debug"] 
