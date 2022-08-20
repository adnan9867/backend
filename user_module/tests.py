import pytest
import requests
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient
from user_module.models import User


@pytest.fixture
def api_client():
    user = User.objects.create(username='john', email='js@js.com', password='js.sj', phone='9080',
                               full_name='ji')
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    return client


# def get_jwt_token():
#     user = User(username='TestUsername', email='testemail@gmail.com',
#                 phone="09890980", full_name="Test Name")
#     user.save()
#     refresh = RefreshToken.for_user(user)  # generate JWT token
#     access_token = str(refresh.access_token),
#
#     return access_token[0]


@pytest.mark.django_db
def test_list_articles(api_client):
    # token = get_jwt_token()
    token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjYxMDkyOTAwLCJqdGkiOiIwY2RiODg0MDNjZjM0NjMwOGQ5MjU5ZGE2YWYzM2JjOSIsInVzZXJfaWQiOjE1fQ.ZosC-_GEk1cwYJ0zgqrZ7S0zDbg5MiiBXfeNdlywNVA'
    headers = {'Authorization': 'Bearer{}'.format(token)}
    url = reverse('post_listing')
    response = api_client.get(url)
    assert response.status_code == 200
