from time import sleep
from django.core.mail import send_mail
from stock_test.celery import app
from .models import Product


@app.task
def send(category):
    sleep(3)
    subject = f'PRODUCTS OF {category}'
    send_mail(subject, 'LIST OF PRODUCTS', None, ['example@gmail.com'])
    return 'Success'