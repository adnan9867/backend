import json

import pytest
import requests
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient
from user_module.models import User


@pytest.fixture
def api_client():
    user = User.objects.create(username='test1', email='test1@gmail.com', password='js.sj', phone='9080',
                               full_name='Test')
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    return client


@pytest.mark.django_db
def test_list_articles(api_client):
    url = reverse('post_listing')
    response = api_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_signup(api_client):
    valid_payload = {
        "email": "test@gmail.com",
        'username': "9779",
        "password": "1234",
        "full_name": "Adnan",
        "phone": "908890890"
    }
    url = reverse('sign_up')
    response = api_client.post(url, data=json.dumps(valid_payload), content_type='application/json', )
    print(response.json())
    assert response.status_code == 200


@pytest.mark.django_db
def test_login(api_client):
    user = User(username='test', email='test@gmail.com', phone='9080',
                full_name='Test')
    user.set_password('1234')
    user.save()
    valid_payload = {
        "email": "test@gmail.com",
        "password": "1234",
    }
    url = reverse('login')
    response = api_client.post(url, data=json.dumps(valid_payload), content_type='application/json', )
    print(response.json())
    assert response.status_code == 200
