import pytest
from django.urls import reverse
from faker import Faker

fake = Faker()

from wallet.tests.factories import categories, subcategories, random_datetime
from random import choice
from wallet.models.category import Category
from wallet.models.sub_category import SubCategory
from wallet.models.expense import Expense
from wallet.models.wallet import Wallet
from wallet.models.comment_expense import ExpenseComment
from django.core import mail


# # # expense_detail views GET test with the use of factory
@pytest.mark.django_db
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
@pytest.mark.django_db
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
@pytest.mark.django_db
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
def test_expense_update(client, create_user, test_password):
    user = create_user()
    wallet = Wallet.objects.create(
        name=fake.word(),
        # users = [user.id]
        )
    wallet.users.set([user])
    cat = Category.objects.create(
        name = fake.word()
    )

    subcat = SubCategory.objects.create(
        name = fake.word(),
        category = cat
    )

    client.login(username=user.username, password=test_password)
    expense = Expense.objects.create(
        amount = fake.pydecimal(3, 2, True),
        member = user,
        category = cat,
        sub_category = subcat,
        comment = fake.text(),
        wallet = wallet
    )
    print(expense)
    print(Expense.objects.count())

    new_decimal = fake.pydecimal(4, 2, True)

    url = reverse('wallet:update_expense', args=[wallet.id, expense.id])

    response = client.post(url, {'amount': new_decimal, 'sub_category': subcat})
    content = response.content.decode('utf-8')
    print(content)

    assert response.status_code == 200  #
    assert str(Expense.objects.get(id=expense.id).amount) not in content


@pytest.mark.django_db
def test_expense_delete(create_expense):
    expense, client, user = create_expense

    url = reverse('wallet:delete_expense', args=[expense.wallet.id, expense.id])

    response = client.post(url)

    content = response.content.decode('utf-8')

    print(content)
    assert response.status_code == 302
    assert Expense.objects.count() == 0



@pytest.mark.django_db
def test_add_comment(create_expense, auto_login_user):
    expense, client, user = create_expense

    client, user = auto_login_user(user=user)

    url = reverse('wallet:expense_comment', kwargs={
        'expense_id': expense.id 
        })

    body_fake = fake.text()
    form_data = {
        'name': 'John Doe',
        'email': 'john@example.com',
        'body': body_fake
    }

    response = client.post(url, data=form_data)

    assert response.status_code == 200

    assert ExpenseComment.objects.count() == 1

    detail_url = reverse('wallet:expense_detail', kwargs={
        'wallet_id': expense.wallet.id,
        'expense_id': expense.id 
        })

    detail_response = client.get(detail_url)
    content = detail_response.content.decode('utf-8')
    print(content)

    assert detail_response.status_code == 200
    assert form_data['name'] in content
    assert form_data["body"] in content # strip method is used for correct assertions



@pytest.mark.django_db
def test_comment_validation(create_expense, auto_login_user):
    expense, client, user = create_expense

    # Log in the user
    client, user = auto_login_user(user=user)

    url = reverse('wallet:expense_comment', kwargs={
        'expense_id': expense.id
    })


    form_data = {
        'name': '',
        'email': 'invalid_email',
        'body': ''
    }

    response = client.post(url, data=form_data)
    content = response.content.decode('utf-8')
    print(content)

    assert 'This field is required' in content
    assert 'Enter a valid email address' in content



@pytest.mark.django_db
def test_share(create_expense, auto_login_user):
    expense, client, user = create_expense

    # Log in the user
    client, user = auto_login_user(user=user)

    url = reverse('wallet:expense_share', kwargs={
        'wallet_id': expense.wallet.id,
        'expense_id': expense.id
    })

    response = client.get(url)

    assert response.status_code == 200

    email_data = {
        'name': 'John Doe',
        'email': 'john@example.com',
        'to': 'eddy.di@yandex.com',
        'comments': 'Check this out!'
    }

    response = client.post(url, data=email_data)
    content = response.content.decode('utf-8')
    print(content)


    assert response.status_code == 200

    # Check if the email was sent
    assert len(mail.outbox) == 1
    sent_email = mail.outbox[0]
    print(sent_email.subject)
    assert sent_email.subject == f"John Doe recommends you to look at {expense.amount}"
    print(sent_email.body)
    assert sent_email.body == f"Look at {expense.amount} at http://testserver{expense.get_detail_url()}\n\nJohn Doe's comments: Check this out!"
