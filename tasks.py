from celery import Celery
import requests
import os
import json


app = Celery('hello',
             broker='amqp://guest@rabbit//',
             backend='amqp://guest@rabbit//',
             )

app.conf.update(
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],  # Ignore other content
    CELERY_RESULT_SERIALIZER='json',
)

@app.task
def  hello(world):
    return world

@app.task
def sales_commit(product, amount, account, transaction):
    web3_host = os.environ.get('SALES_COMMIT')
    print('&&&&&')
    print(web3_host)
    data = {
        'product_id': product,
        'amount': amount,
        'account_id': account,
        'transaction_id': transaction
    }
    web3_res = requests.post(url=web3_host, data=json.dumps(data), headers={'content-type': 'application/json'})
    print('******')
    print(web3_res.json())
    if web3_res.status_code in [200, 201, 202] :
        taf_host = os.environ.get('GENERATE_COMMISSION')
        taf_res = requests.post(url=taf_host, data=data)
        if taf_res.status_code == 200:
            return True

    return False

@app.task
def commission_commit(account, commission):
    web3_host = os.environ.get('COMMISSION_COMMIT')
    data = {
        'account_id': account,
        'number': commission
    }
    web3_res = requests.post(url=web3_host, data=json.dumps(data), headers={'content-type': 'application/json'})
    print('******')
    print(web3_res.json())
    if web3_res.status_code in [200, 201, 202]:
        return True
    return False


@app.task
def get_total_commission(account):
    web3_host = os.environ.get('GET_COMMISSION')
    web3_host = web3_host.format(account)
    web3_res = requests.get(url=web3_host)
    if web3_res.status_code in [200, 201, 202]:
        data = web3_res.json()
        taf_host = os.environ.get('POST_COMMISSION')
        taf_res = requests.post(url=taf_host, data=json.dumps(data), headers={'content-type': 'application/json'})
        if taf_res.status_code in [200, 201, 202]:
            return True
    return False
