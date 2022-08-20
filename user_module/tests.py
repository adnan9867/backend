import pytest

from django.urls import reverse


@pytest.mark.django_db
def test_list_articles(client):
    url = reverse('post_listing')
    response = client.get(url)
    assert response.status_code == 200
