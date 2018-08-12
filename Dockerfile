FROM python:3.6
MAINTAINER Sharad Baidya

COPY . /home/docker/celery/
RUN pip install -r /home/docker/celery/requirements.txt

WORKDIR /home/docker/celery/
