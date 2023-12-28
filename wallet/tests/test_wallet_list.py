from django.urls import reverse


def test_wallet_list(create_wallet_and_add_user):
    client, wallet, user = create_wallet_and_add_user()
    url = reverse('wallet:wallet_list')
    response = client.get(url)
    # print(wallet)
    # print(user)
    assert wallet.users.count() == 1
    assert wallet.users.first() == user
    assert response.status_code == 200