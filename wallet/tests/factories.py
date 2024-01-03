import factory

from faker import Faker
fake = Faker()

from django.contrib.auth.models import User
from wallet.models.wallet import Wallet
from wallet.models.category import Category
from wallet.models.sub_category import SubCategory
from wallet.models.income import Income
from wallet.models.expense import Expense
from random import choice, randint
from datetime import datetime, timedelta

def random_datetime(start_date=None, end_date=None):
    if not start_date:
        start_date = datetime.now() - timedelta(days=365)  # One year ago by default
    if not end_date:
        end_date = datetime.now()

    delta = end_date - start_date
    random_days = randint(0, delta.days)
    random_seconds = randint(0, 24 * 60 * 60 - 1)  # One day in seconds

    return start_date + timedelta(days=random_days, seconds=random_seconds)

categories = [
    "Electronics",
    "Clothing",
    "Home and Garden",
    "Books",
    "Sports and Outdoors",
    "Toys and Games",
    "Health and Beauty",
    "Automotive",
    "Food and Grocery",
    "Movies and Music",
    "Furniture",
    "Jewelry",
    "Pet Supplies",
    "Computers",
    "Office Supplies",
    "Baby Products",
    "Fitness",
    "Travel",
    "Crafts and Hobbies",
    "Outdoor Gear",
]
subcategories = [
    "Smartphones",
    "Laptops",
    "Headphones",
    "T-Shirts",
    "Jeans",
    "Bedding",
    "Cookware",
    "Mystery Novels",
    "Yoga Mats",
    "Board Games",
    "Dermatology Products",
    "Car Accessories",
    "Cereal",
    "Action Movies",
    "Classical Music",
    "Sofas",
    "Earrings",
    "Dog Food",
    "Gaming PCs",
    "Notebooks",
    "Pacifiers",
    "Dumbbells",
    "Travel Backpacks",
    "Knitting Supplies",
    "Camping Tents",
    "Fitness Trackers",
    "Beach Towels",
    "Blenders",
    "Winter Jackets",
    "Gardening Tools",
    "Children's Books",
    "Baseball Gear",
    "Building Blocks",
    "Facial Cleansers",
    "Car Care Kits",
    "Pasta",
    "Animated Movies",
    "Rock Music",
    "Coffee Tables",
    "Bracelets",
    "Cat Toys",
    "Gaming Consoles",
    "Desktop Monitors",
    "Baby Formula",
    "Weightlifting Gloves",
    "Travel Pillows",
    "Painting Supplies",
    "Hiking Boots",
    "Fitness DVDs",
    "Travel Adapters",
    "Sewing Machines",
    "Sleeping Bags",
    "Jump Ropes",
    "Portable Grills",
    "Fitness Apparel",
    "Wine Glasses",
    "Candles",
    "Tea",
    "Horror Movies",
    "Country Music",
    "Bookshelves",
    "Necklaces",
    "Bird Feed",
    "VR Headsets",
    "Wireless Keyboards",
    "Diapers",
    "Resistance Bands",
    "Travel Blankets",
    "Drawing Pencils",
    "Backpacks",
    "Canvases",
    "Trekking Poles",
    "Yoga DVDs",
    "Travel Mugs",
    "Watercolor Paints",
    "Sleeping Pads",
    "Exercise Bikes",
    "Sunscreen",
    "Carabiners",
    "Board Shorts",
    "Juicers",
    "Smoothie Blenders",
    "Historical Fiction",
    "Puzzle Games",
    "Crossword Puzzles",
    "Dog Beds",
    "Wireless Earbuds",
    "Rain Jackets",
    "Garden Decor",
    "Romantic Comedies",
    "Jazz Music",
    "Side Tables",
    "Watches",
    "Aquarium Supplies",
    "Snowboards",
    "Home Gyms",
    "Travel Guides",
    "Crochet Hooks",
]


class UserFactory(factory.django.DjangoModelFactory):
	class Meta:
		model = User
	
	username = fake.name()
	is_staff = 'True'


class WalletFactory(factory.django.DjangoModelFactory):
    users = [factory.SubFactory(UserFactory)]

    class Meta:
        model = Wallet

    name = fake.word()

    @factory.post_generation
    def users(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for user in extracted:
                self.users.add(user)


class CategoryFactory(factory.django.DjangoModelFactory):
    name = choice(categories)
	
    class Meta:
        model = Category
	

class SubCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SubCategory
    
    name = choice(subcategories)
    category = factory.SubFactory(CategoryFactory) # this part shows that the subcategory is linked with category with relationship FK

    @factory.post_generation
    def category(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for category in extracted:
                self.category.add(category)


# class ExpenseFactory(factory.django.DjangoModelFactory):
    # amount = fake.pydecimal(3, 2, True)
    # created_at = random_datetime()
    # comment = fake.text()
    # category = CategoryFactory().create()
    # sub_category = None
    # sub_category.category = category
    # wallet = None
    # member = None
    # 
    # class Meta:
        # model = Expense
    
