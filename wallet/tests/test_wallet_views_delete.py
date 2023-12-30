import pytest 
from django.urls import reverse
from faker import Faker
from wallet.models.wallet import Wallet


fake = Faker()


@pytest.mark.django_db
def test_wallet_create(api_client, create_user):
    user = create_user()
    api_client.force_authenticate(user=user)

    # part for checking POST requests
    list_url = reverse('wallet-api:wallet_list')

    data = {
        'name': user.username + ' test-wallet',
        'users': [user.id]
    }
    response_create = api_client.post(list_url, data=data, format='json')
    print(response_create.data)

    assert response_create.status_code == 201  # Assuming you expect a created status code
    assert response_create.data['name'] == user.username + ' test-wallet'
    assert user.id in response_create.data['users']

    # part for checking GET requests
    detail_url = reverse('wallet-api:wallet_detail', args=[response_create.data['id']])
    
    response_get = api_client.get(list_url)
    response_get_detail = api_client.get(detail_url)

    assert response_get.status_code == 200
    assert response_get_detail.status_code == 200
    
    # part for checking PATCH requests
    patch_data = {
        'name': fake.name() + ' changed test wallet'
    }

    patched_response = api_client.patch(detail_url, data=patch_data)

    print(patched_response.data)

    assert patched_response.status_code == 200
    assert patched_response.data['name'] != response_create.data['name']
    
    # part for checking DELETE requests
    delete_response = api_client.delete(detail_url)

    try:
        Wallet.objects.get(id=response_create.data['id'])
    except Wallet.DoesNotExist as e:
        print(e)

    assert delete_response.status_code == 204

    api_client.force_authenticate(user=None)