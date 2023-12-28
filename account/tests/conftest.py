import uuid
import pytest

from wallet.models.wallet import Wallet
from faker import Faker

fake = Faker()

# from django.contrib.auth.models import User

# @pytest.fixture()
# def user_1(db):
    # user = User.objects.create_user("test-user")
    # print('create-user')
    # return user

# human_names = ["Alice", "Bob", "Charlie", "Diana", "Edward", "Fiona", "George", "Hannah", "Ian", "Julia"]
# last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Garcia", "Rodriguez", "Martinez"]
# usernames = ["alice123", "bob456", "charlie789", "diana_92", "edward_m", "fiona22", "george75", "hannah_34", "ian1980", "julia_k"]
# emails = [f"{name.lower()}_{last.lower()}@example.com" for name, last in zip(human_names, last_names)]

# @pytest.fixture
# def new_user_factory(db):
    # def create_app_user(
        # username: str,
        # password: str = None,
        # first_name: str = "firstname",
        # last_name: str = "lastname",
        # email: str = "test@test.com",
        # is_staff: str = False,
        # is_superuser: str = False,
        # is_active: str = True,
    # ):
        # user = User.objects.create_user(
            # username=username,
            # password=password,
            # first_name=first_name,
            # last_name=last_name,
            # email=email,
            # is_staff=is_staff,
            # is_superuser=is_superuser,
            # is_active=is_active,
        # )
        # return user
    # return create_app_user


# @pytest.fixture
# def new_user2(db, new_user_factory):
    # return new_user_factory("Test_user","password", "MyName", is_staff="True")

from pytest_factoryboy import register # helps with registering factories

from account.tests.factories import UserFactory, CategoryFactory, SubCategoryFactory

register(UserFactory) # fixture for the access of the created UserFactory will be under user_factory
register(CategoryFactory) # alias category_factory
register(SubCategoryFactory) # alias sub_category_factory

# @pytest.fixture
# def new_category(db, category_factory):
    # category = category_factory.create()
    # return category

@pytest.fixture
def test_password():
   return 'strong-test-pass'

@pytest.fixture
def create_user(db, django_user_model, test_password):
   def make_user(**kwargs):
       kwargs['password'] = test_password
       if 'username' not in kwargs:
           kwargs['username'] = fake.name()
       return django_user_model.objects.create_user(**kwargs)
   return make_user

@pytest.fixture
def auto_login_user(db, client, create_user, test_password):
   def make_auto_login(user=None):
       if user is None:
           user = create_user(username='someone') 
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
