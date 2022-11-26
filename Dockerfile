FROM python:3.9.9-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get -y install libpq-dev gcc cron \
    && pip install psycopg2

RUN pip install poetry
COPY . /app/

RUN poetry export --dev -f requirements.txt --output requirements.txt --without-hashes
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /app/var/log
RUN touch /app/var/log/cron.log

COPY run.sh /app/run.sh

EXPOSE 8000

CMD /app/run.sh
