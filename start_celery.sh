#!/usr/bin/env bash
source env.sh
celery -A tasks  worker -l info