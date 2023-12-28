# from django.test import TestCase
import pytest
from django.contrib.auth.models import User
from wallet.models.sub_category import SubCategory

# @pytest.fixture(scope="session")
# def fixture_1():
    # print('run fixture_1')
    # return 1
# 
# def test_example1(fixture_1):
    # print('run example1')
    # num = fixture_1
    # assert num == 1
# 
# def test_example2(fixture_1):
    # print('run example2')
    # num = fixture_1
    # assert num == 1

# @pytest.fixture
# def yield_fixture():
    # print('Start of test phase')
    # yield 6
    # print('End of test phase')
# 
# def test_example1(yield_fixture):
    # print('run example')
    # assert yield_fixture == 6


# @pytest.mark.django_db
# def test_user_create():
    # User.objects.create_user('test', 'test@test.com', 'test')
    # count = User.objects.all().count()
    # print(count)
    # assert count == 1
# 
# @pytest.mark.django_db
# def test_user_create1():
#    count = User.objects.all().count()
#    print(count)
#    assert count == 0


# @pytest.fixture()
# def user_1(db): # db parameter is bringing in the db into function
    # return User.objects.create_user("test-user")

# @pytest.mark.django_db
# def test_set_check_password(user_1):
    # user_1.set_password("new-password")
    # assert user_1.check_password("new-passwords") is True

# 
# def test_set_check_password1(user_1):
    # print('check-user1')
    # assert user_1.username == "test-user"
# 
# def test_set_check_password2(user_1):
    # print('check-user2')
    # assert user_1.username == "test-user"

# def test_new_user(new_user):
    # users = [print(i.first_name) for i in new_user]
    # assert len(users) == 10 

# # making a simple test to see if the name is being generated
# def test_new_user(user_factory):
	# print(user_factory.username)
	# assert True # that will pass all the things that are being called or executed in test

# # build() function used
# def test_new_user(user_factory):
	# user = user_factory.build()
	# print(user.username)
	# assert True

# # create() function used
# @pytest.mark.django_db
# def test_new_user1(user_factory):
	# user = user_factory.create()
	# print(user.username)
	# assert True


# # build() function used
# @pytest.mark.django_db
# def test_new_user(user_factory):
	# user = user_factory.build()
	# count = User.objects.all().count()
	# print(count)
	# print(user.username)
	# assert True

# # create() function used
# @pytest.mark.django_db
# def test_new_user1(user_factory):
	# user = user_factory.create()
	# count = User.objects.all().count()
	# print(count)
	# print(user.username)
	# assert True

# # testing build part
# def test_sub_cat(sub_category_factory):
    # sub_cat = sub_category_factory.build()
    # print(sub_cat.name)
    # assert True

# # testing create
# def test_sub_cat_db(db, sub_category_factory):
    # sub_cat = sub_category_factory.create()
    # print(sub_cat.category)
    # assert True


# @pytest.mark.parametrize(
    # 'name, category, validity',
    # [
        # ('Lunch', 1, True),
        # ('Breakfast', 1, True),
        # ('Dinner', 1, True),
    # ]
# )
# def test_sub_cat(
    # db, sub_category_factory, name, category, validity
# ):
    # test = sub_category_factory(
        # name = name,
        # category_id = category,
    # )
# 
    # item = SubCategory.objects.all().count()
    # assert item == validity
    # assert test.category.name == 'food'


from django.urls import reverse

# @pytest.mark.django_db
# def test_view(client):
#    url = reverse('account:account_index')
#    response = client.get(url)
#    assert response.status_code == 200


# # checking unauthorized access to normal users wallet list page
# @pytest.mark.django_db
# def test_unauthorized(client):
#    url = reverse('wallet:wallet_list')
#    response = client.get(url)
#    assert response.status_code == 401

# # checking unauthorized access to super users wallet list page
# @pytest.mark.django_db
# def test_superuser_view(admin_client):
#    url = reverse('wallet:wallet_list')
#    response = admin_client.get(url)
#    assert response.status_code == 200

# # checking all pages for account app pages
# @pytest.mark.parametrize('param', [
    # ('account:account_index'),
    # ('account:login'),
    # ('account:login_with_token'),
    # ('account:logout'),
    # ('account:password_change'),
    # ('account:password_change_done'),
    # ('account:password_reset'),
    # ('account:password_reset_done'),
    # ('account:password_reset_confirm'),
    # ('account:password_reset_complete'),
    # ('account:register'),
    # ('account:edit'),
    # ('account:redirect'),
    # ('account:successful_login'),
# ])
# def test_render_views(client, param):
    # url = reverse(param)
    # resp = client.get(url)
    # assert resp.status_code == 200

# # testing django_user_model

# @pytest.mark.django_db
# def test_user_detail(client, django_user_model):
#    user = django_user_model.objects.create(
    #    username='someone', password='password'
#    )
#    url = reverse('account:edit', kwargs={'pk': user.pk})
#    response = client.get(url)
#    assert response.status_code == 200
#    assert 'someone' in response.content

# @pytest.mark.django_db
# def test_auth_view(client, create_user, test_password):
#    user = create_user()
#    url = reverse('account:login')
#    client.login(
    #    username=user.username, password=test_password
#    )
#    response = client.get(url)
#    assert response.status_code == 200


# @pytest.mark.django_db
# def test_auth_view_wallet(client, create_user, test_password):
#    user = create_user()
#    url = reverse('wallet:wallet_list')
#    client.login(
    #    username=user.username, password=test_password
#    )
#    response = client.get(url)
#    assert response.status_code == 302

# @pytest.mark.django_db
# def test_auth_view(auto_login_user):
#    client, user = auto_login_user()
#    url = reverse('account:login')
#    response = client.get(url)
#    assert response.status_code == 302





