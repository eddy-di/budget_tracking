import pytest 
from faker import Faker

from wallet.models.wallet import Wallet
from django.contrib.auth.models import User
from django.urls import reverse
from wallet.tests.factories import WalletFactory

fake = Faker()



# # wallet_list GET test
@pytest.mark.skip
def test_web_wallet_view(client, create_user, test_password):
    user = create_user()

    client.login(username=user.username, password=test_password)

    wallet = Wallet.objects.create(name=fake.word())
    wallet.users.set([user])

    url = reverse('wallet:wallet_list')

    response = client.get(url)
    content = response.content.decode('utf-8')
    print(content)
    assert response.status_code == 200
    assert wallet.name in content
    assert user.username in content



# # testing create_wallet fixture that utilizes two factories # wallet_list GET test
@pytest.mark.skip
def test_wallet_create_with_factory(create_wallet_with_user):
    wallet, client, user = create_wallet_with_user
    url = reverse('wallet:wallet_list')
    response = client.get(url)
    content = response.content.decode('utf-8')
    print(content)
    assert response.status_code == 200



# # wallet_detail view GET test
@pytest.mark.skip
def test_web_wallet_detail(client, create_user, test_password):
    user = create_user()

    client.login(username=user.username, password=test_password)

    wallet = Wallet.objects.create(name=fake.word())
    wallet.users.set([user])

    url = reverse('wallet:wallet_info', args=[wallet.id])

    resp = client.get(url)
    content = resp.content.decode('utf-8')
    print(content)
    assert resp.status_code == 200



# # wallet_add POST test
@pytest.mark.skip
def test_web_wallet_add(client, create_user, test_password):
    user = create_user()

    client.login(username=user.username, password=test_password)

    wallet_name = fake.word()

    data = {
        'name': wallet_name,
        'users': [user.id]
    }

    url = reverse('wallet:add_wallet')

    resp = client.post(url, data=data)
    content = resp.content.decode('utf-8')
    print(content)
    db_wallet = Wallet.objects.get(name=wallet_name)

    assert resp.status_code == 302
    assert db_wallet.name == wallet_name

