import factory

from faker import Faker
fake = Faker()

from django.contrib.auth.models import User
from wallet.models.wallet import Wallet

class UserFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = User
	
	username = fake.name()
	is_staff = 'True'
	
class WalletFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Wallet

    name = fake.word()
    users = factory.SubFactory(UserFactory)