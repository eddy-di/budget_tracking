import factory

from faker import Faker
fake = Faker()

from django.contrib.auth.models import User
from wallet.models.category import Category
from wallet.models.sub_category import SubCategory

class UserFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = User
	
	username = fake.name()
	is_staff = 'True'
	

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
    
    name = 'food'
	

class SubCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SubCategory
    
    name = fake.word()
    category = factory.SubFactory(CategoryFactory)