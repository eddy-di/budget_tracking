import pytest 
from django.urls import reverse


@pytest.mark.django_db
def test_wallet_create(api_client, create_user):
    users = create_user()
    api_client.force_authenticate(user=users)

    url = reverse('wallet-api:wallet_list')
    data = {
        'name': 'test-wallet',
        'users': [users.id]
    }
    response = api_client.post(url, data=data, format='json')
    print(response.data)

    assert response.status_code == 201  # Assuming you expect a created status code
    assert response.data['name'] == 'test-wallet'
    assert users.id in response.data['users']
    api_client.force_authenticate(user=None)