import os
from pathlib import Path

import requests
from py_dotenv import read_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
dotenv_file = os.path.join(BASE_DIR, ".env")
if os.path.isfile(dotenv_file):
    read_dotenv(dotenv_file)


no_of_retries = 3


def make_request(ip_address):
    secret_key = os.environ.get('ABSTRACT_API')
    url = "https://ipgeolocation.abstractapi.com/v1/?api_key={}&ip_address={}".\
        format(secret_key, ip_address)
    for i in range(0, no_of_retries):
        try:
            result = requests.get(url).json()
            if 'country' in result:
                return result['country_code']
            else:
                continue
        except Exception as e:
            continue
    return None


def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

