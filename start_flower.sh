#!/usr/bin/env bash
celery flower -A tasks --broker="amqp://rabbit:5672" --broker_api="http://guest:guest@rabbit:15672/api/"
