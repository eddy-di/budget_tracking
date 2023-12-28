import uuid

from django.test import Client
import pytest
from wallet.models.wallet import Wallet

from rest_framework.authtoken.models import Token

from faker import Faker
fake = Faker()



@pytest.fixture
def test_password(): # name says it all
   return 'strong-test-pass'



@pytest.fixture
def create_user(db, django_user_model, test_password): # initial fixture is used to create a user
   def make_user(**kwargs):
       kwargs['password'] = test_password
       if 'username' not in kwargs:
           kwargs['username'] = fake.name() # or str(uuid.uuid4())
       return django_user_model.objects.create_user(**kwargs)
   return make_user



@pytest.fixture
def auto_login_user(db, client, create_user, test_password): # utilizes bith previous fixtures to allow to authenticate
   def make_auto_login(user=None):
       if user is None:
           user = create_user(username='someone') # username='someone', password='something'
       client.login(username=user.username, password=test_password)
       return client, user
   return make_auto_login



@pytest.fixture
def create_wallet_and_add_user(db, create_user, client):
    def make_wallet_with_user(**wallet_kwargs):
        user = create_user()
        wallet_defaults = {
            'name': 'Test Wallet',
            'slug': 'test-wallet',
        }
        wallet_defaults.update(wallet_kwargs)
        wallet = Wallet.objects.create(**wallet_defaults)
        wallet.users.add(user)
        
        client.login(username=user.username, password='strong-test-pass')
        
        return client, wallet, user

    return make_wallet_with_user



@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()



@pytest.fixture
def get_or_create_token(db, create_user, api_client):
    user = create_user()

    api_client.login(username=user.username, password=test_password)

    token, _ = Token.objects.get_or_create(user=user)
    # print(token, _)
    return token


@pytest.fixture
def api_client_with_credentials(
   db, create_user, api_client
):
   user = create_user()
   api_client.force_authenticate(user=user)
   yield api_client
   api_client.force_authenticate(user=None)