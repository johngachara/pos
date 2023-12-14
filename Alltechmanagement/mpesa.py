import json
from base64 import b64encode
from datetime import datetime

import requests
from requests.auth import HTTPBasicAuth

from djangoProject15 import settings


def get_access_token():
    url = settings.MPESA_API["CREDENTIALS_URL"]
    consumer_key = settings.MPESA_API["CONSUMER_KEY"]
    consumer_secret = settings.MPESA_API["CONSUMER_SECRET"]
    auth = HTTPBasicAuth(consumer_key, consumer_secret)
    try:
        response = requests.get(url, auth=auth)
    except Exception as err:
        raise err
    else:
        token = response.json()["access_token"]
        return token



def get_current_timestamp():
    return datetime.now().strftime('%Y%m%d%H%M%S')


def generate_request_headers():
    token = get_access_token()
    return {"Authorization": f"Bearer {token}"}

def get_payment_url():
    return settings.MPESA_API["PAYMENT_URL"]


def get_callback_url():
    return settings.MPESA_API["CALLBACK_URL"]
