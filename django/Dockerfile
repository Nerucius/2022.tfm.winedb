FROM python:3-alpine

RUN mkdir /app
WORKDIR /app

# Setup build for uWSGI + PostgreSQL
RUN apk add gcc make libc-dev musl-dev linux-headers pcre-dev postgresql-dev

# Copy and install python deps
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install --no-cache-dir uwsgi

# Copy and install django app
COPY . .

WORKDIR /app
RUN chmod a+x docker-entrypoint.sh
ENTRYPOINT [ "sh", "-c", "./docker-entrypoint.sh" ]
