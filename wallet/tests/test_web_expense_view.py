import pytest
from django.urls import reverse
from faker import Faker

fake = Faker()

from wallet.tests.factories import categories, subcategories, random_datetime
from random import choice
from wallet.models.category import Category
from wallet.models.sub_category import SubCategory
from wallet.models.expense import Expense


# # # expense_detail views GET test with the use of factory
@pytest.mark.skip
def test_expense_detail(create_expense):
    expense, client, user = create_expense
    print(expense.wallet.id)
    # client.login(username=expense.member.username, password=test_password)
    url = reverse('wallet:expense_detail', args=[expense.wallet.id, expense.id])

    resp = client.get(url)
    content = resp.content.decode('utf-8')
    print(content)

    assert resp.status_code == 200



# # # expense_list views GET test with the use of factory or fixture
@pytest.mark.skip
def test_expense_list(create_expense):
    expense, client, user = create_expense # makes an individual expense instance
    url = reverse('wallet:expense_list', args=[expense.wallet.id])
    response = client.get(url)
    content = response.content.decode('utf-8')
    print(content)
    assert response.status_code == 200
    assert str(expense.amount) in content
    assert expense.comment in content



# # # test expense_add view POST successful
@pytest.mark.skip
def test_expense_add(create_wallet_with_user):
    wallet, client, user = create_wallet_with_user
    url = reverse('wallet:add_expense', args=[wallet.id])
    
    cat = Category.objects.create(name=choice(categories))
    subcat = SubCategory.objects.create(
        name=choice(subcategories), 
        category=cat
        )
    test_amount = fake.pydecimal(3, 2, True)

    data = {
        'amount': test_amount,
        'currency': 1,
        'comment': fake.text(),
        'wallet': wallet.id,
        'category': cat.id,
        'sub_category': subcat.id,
        'member': user.id
    }

    response = client.post(url, data=data)
    new_expense = Expense.objects.get(amount=test_amount)
    print(new_expense)
    assert response.status_code == 302
    assert new_expense.amount == test_amount
    assert new_expense.currency == 1
    assert new_expense.comment == data['comment']
    assert new_expense.wallet == wallet
    assert new_expense.category == cat
    assert new_expense.sub_category == subcat
    assert new_expense.member.username == user.username



@pytest.mark.django_db
def test_expense_update(create_expense):
    # # # example of created expense instance
    expense, client, user = create_expense
    print(expense)
    url = reverse('wallet:update_expense', args=[expense.wallet.id, expense.id])   
    # # # checking the update from patch for response
    patched_decimal = fake.pydecimal(4, 2, True)
    data = {
        'amount': patched_decimal
    }

    patched_response = client.patch(url, data=data)
    print(expense)
    patched_content = patched_response.content.decode('utf-8')

    patched_string = '{0:f}'.format(patched_decimal)
    print(patched_decimal)
    print(patched_content)

    assert patched_response.status_code == 201
    assert patched_decimal != expense.amount
