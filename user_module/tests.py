import json

import pytest
import requests
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient
from user_module.models import User, Post


@pytest.fixture
def api_client():
    user = User.objects.create(username='test1', email='test1@gmail.com', password='js.sj', phone='9080',
                               full_name='Test')
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    return client


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
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_profile(api_client):
    url = reverse('get_user_profile')
    response = api_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_post(api_client):
    valid_payload = {
        "title": "Test Title",
        "content": "Here is Content",
    }
    url = reverse('post')
    response = api_client.post(url, data=json.dumps(valid_payload), content_type='application/json', )
    print(response.json())
    assert response.status_code == 200


@pytest.mark.django_db
def test_update_post(api_client):
    valid_payload = {
        "title": "Test Title",
        "content": "Here is Content",
    }
    url = reverse('post')
    response = api_client.post(url, data=json.dumps(valid_payload), content_type='application/json', )
    print(response.json())
    data = response.json()
    valid_payload = {
        "title": "Test Title",
        "content": "Here is Content",
        'id': data['data']['id']
    }
    url = reverse('update_post')
    response = api_client.put(url, data=json.dumps(valid_payload), content_type='application/json', )
    print(response.json())
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_post(api_client):
    valid_payload = {
        "title": "Test Title",
        "content": "Here is Content",
    }
    url = reverse('post')
    response = api_client.post(url, data=json.dumps(valid_payload), content_type='application/json', )
    print(response.json())
    data = response.json()
    pk = data['data']['id']
    url = reverse('delete_post')
    response = api_client.delete(url + '?id={}'.format(pk))
    print(response.json())
    assert response.status_code == 200


@pytest.mark.django_db
def test_all_post_listing(api_client):
    url = reverse('post_listing')
    response = api_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_like_post(api_client):
    valid_payload = {
        "title": "Test Title",
        "content": "Here is Content",
    }
    url = reverse('post')
    response = api_client.post(url, data=json.dumps(valid_payload), content_type='application/json', )
    print(response.json())
    data = response.json()
    valid_payload = {
        'post': data['data']['id']
    }
    url = reverse('post_like')
    response = api_client.post(url, json.dumps(valid_payload), content_type='application/json', )
    print(response.json())
    assert response.status_code == 200
