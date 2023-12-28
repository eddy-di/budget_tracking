import pytest

from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

@pytest.mark.parametrize('urls', [
    ('wallet_api:expense_list'),
    ('wallet_api:income_list'),
    ('wallet_api:wallet_list'),
    ('wallet_api:invite'),
])
@pytest.mark.django_db
def test_unauthorized_request_endpoints_token(api_client_with_credentials, urls):
    url = reverse(urls)
    # token = get_or_create_token
    # user = User.objects.create_user('test', 'user@example.com', 'Strong-test-pass')
    # token = Token.objects.create(user=user)
    # print(token)
    # api_client.credentials(HTTP_AUTHORIZATION='Token: ' + token.key)
    response = api_client_with_credentials.get(url)
    assert response.status_code == 200