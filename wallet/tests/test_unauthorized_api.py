import pytest

from django.urls import reverse


# @pytest.mark.django_db
@pytest.mark.parametrize('param', [
    ('wallet_api:expense_list'),
    ('wallet_api:income_list'),
    ('wallet_api:wallet_list'),
    ('wallet_api:invite'),
    # ('wallet_api:expense_detail'), #
    # ('wallet_api:income_detail'), #
    # ('wallet_api:wallet_detail'), #
    # ('wallet_api:join_wallet'), #
])
def test_unauthorized_request_endpoints(api_client, param):
    url = reverse(param)
    response = api_client.get(url)
    assert response.status_code == 401