FROM python:3.6-alpine

# Log directory to sync files to
ENV RDS_LOG_DIR "/rds-logs"
WORKDIR /rds-logs

RUN apk add --no-cache bash

WORKDIR /usr/src/app
ADD requirements.txt .
RUN pip install -r requirements.txt

ADD sync.py .

COPY docker-entrypoint.sh /usr/local/bin
ENTRYPOINT ["docker-entrypoint.sh"]

CMD ["sync"]
