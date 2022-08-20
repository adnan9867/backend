import os
from pathlib import Path
import datetime
import requests
from py_dotenv import read_dotenv

from user_module.models import UserHolidayInfo

BASE_DIR = Path(__file__).resolve().parent.parent
dotenv_file = os.path.join(BASE_DIR, ".env")
if os.path.isfile(dotenv_file):
    read_dotenv(dotenv_file)

no_of_retries = 3


def get_location(ip_address):
    secret_key = os.environ.get('ABSTRACT_API')
    url = "https://ipgeolocation.abstractapi.com/v1/?api_key={}&ip_address={}". \
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


def get_holiday(country):
    secret_key = '093aa27915024a668a7585dfa35e279e'
    current_date = datetime.datetime.now().date()
    year = str(current_date)[:4]
    month = str(current_date)[5:7]
    days = str(current_date)[8:]
    url = "https://holidays.abstractapi.com/v1/?api_key={}&country={}&year={}&month={}&day={}".format(secret_key,
                                                                                                      country, year,
                                                                                                      month, days)
    for i in range(0, no_of_retries):
        try:
            result = requests.get(url).json()
            if 'location' in result[0]:
                return result[0]
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


def user_holiday_info(user=None, request=None):
    ip = get_ip(request)
    if ip:
        location = 'US'
        if location:
            holiday = get_holiday(country=location)
            if holiday:
                UserHolidayInfo.objects.create(user=user, country=holiday['location'],
                                               day_name=holiday['name'], type=holiday['type'])
                return None

    return None
