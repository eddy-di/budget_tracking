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
    response = api_client_with_credentials.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize('email, password, verify_code', [
    ('', [], 400),
    ((), 'strong_pass', 400),#
    ('user@example.com', [], 400),#
    # ('user@example.com', 'invalid_pass', 400),
    # ('user@example.com', 'strong-test-pass', 200), #
])
def test_login_data_validation(
    email, password, verify_code, create_user, api_client
):
    user = create_user(username='user@example.com', password='strong-test-pass').save()
    url = reverse('token_obtain_pair')
    data = {
        'username':email,
        'password':password
    }
    response = api_client.post(url, data=data)
    print(response)
    assert response.status_code == verify_code