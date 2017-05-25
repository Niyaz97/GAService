FROM ubuntu:16.10
MAINTAINER GAService team

WORKDIR /GAService

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y -q \
	python3 \
        python3-dev \
        python3-setuptools \
        python3-pip \
        libpq-dev \
        nginx \
        build-essential \
        supervisor \
        sqlite3  && \
        pip3 install -U pip setuptools


COPY requirements.txt /tmp/
RUN pip3 install --requirement /tmp/requirements.txt

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 80

