import pytest 
from django.urls import reverse
from faker import Faker


fake = Faker()


@pytest.mark.django_db
def test_wallet_create(api_client, create_user):
    user = create_user()
    api_client.force_authenticate(user=user)

    list_url = reverse('wallet-api:wallet_list')

    data = {
        'name': user.username + ' test-wallet',
        'users': [user.id]
    }
    response_create = api_client.post(list_url, data=data, format='json')
    print(response_create.data)
    
    detail_url = reverse('wallet-api:wallet_detail', args=[response_create.data['id']])
    print(detail_url)

    assert response_create.status_code == 201  # Assuming you expect a created status code
    assert response_create.data['name'] == user.username + ' test-wallet'
    assert user.id in response_create.data['users']



    api_client.force_authenticate(user=None)