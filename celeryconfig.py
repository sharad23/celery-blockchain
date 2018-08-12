BROKER_URL = 'amqp://guest:guest@localhost:5672//'
CELERY_IMPORTS = ('tasks', )

CELERY_RESULT_BACKEND = 'amqp'