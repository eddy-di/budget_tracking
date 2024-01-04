import pytest
from django.urls import reverse
from faker import Faker

fake = Faker()

from wallet.models.income import Income
from wallet.models.comment_income import IncomeComment
from django.core import mail



# # # test web income list
@pytest.mark.django_db
def test_income_list_get(create_income):
    income, client, user = create_income

    url = reverse('wallet:income_list', args=[income.wallet.id])
    
    response = client.get(url)
    content = response.content.decode('utf-8')
    
    assert response.status_code == 200
    assert income.comment in content



# # # test web income detail
@pytest.mark.django_db
def test_income_add_post(create_wallet_with_user, subcat_with_cat):
    wallet, client, user = create_wallet_with_user
    cat, subcat = subcat_with_cat

    url = reverse('wallet:add_income', args=[wallet.id])

    add_decimal = fake.pydecimal(3, 2, True)
    add_comment = fake.text()

    data = {
        'amount': add_decimal,
        'comment': add_comment,
        'wallet': wallet.id,
        'category': cat.id,
        'sub_category': subcat.id,
        'member': user.id
    }

    response = client.post(url, data)
    content = response.content.decode('utf-8')

    assert response.status_code == 200
    assert str(add_decimal) in content
    assert add_comment in content



# # # test web income detail
@pytest.mark.django_db
def test_income_detail_get(create_income):
    income, client, user = create_income
    url = reverse('wallet:income_detail', args=[income.wallet.id, income.id])
    response = client.get(url)
    content = response.content.decode('utf-8')
    print(content)
    assert response.status_code == 200
    assert income.comment in content
    assert str(income.amount) in content



# # # test web income update
@pytest.mark.django_db
def test_income_update_post(create_income):
    income, client, user = create_income
    url = reverse('wallet:update_income', args=[income.wallet.id, income.id])


    new_decimal = fake.pydecimal(4, 2, True)
    new_comment = fake.text()

    data = {
        'amount': new_decimal,
        'comment': new_comment
    }

    response = client.post(url, data)
    content = response.content.decode('utf-8')

    assert response.status_code == 200
    assert str(new_decimal) in content
    assert new_comment in content



# # # test web income delete
@pytest.mark.django_db
def test_income_delete_post(create_income):
    income, client, user = create_income

    url = reverse('wallet:delete_income', args=[income.wallet.id, income.id])

    response = client.post(url)
    content = response.content.decode('utf-8')

    assert response.status_code == 302
    assert Income.objects.count() == 0



# # # test web income comment
@pytest.mark.django_db
def test_income_comment(create_income, auto_login_user):
    income, client, user = create_income

    url = reverse('wallet:income_comment', kwargs= {
        'income_id': income.id
    })

    body_fake = fake.text()
    form_data = {
        'name': 'John Doe',
        'email': 'john@example.com',
        'body': body_fake
    }

    response = client.post(url, data=form_data)

    assert response.status_code == 200
    assert IncomeComment.objects.count() == 1

    detail_url = reverse('wallet:income_detail', kwargs= {
        'wallet_id': income.wallet.id,
        'income_id': income.id
    })

    detail_response = client.get(detail_url)
    content = detail_response.content.decode('utf-8')

    assert detail_response.status_code == 200
    assert form_data['name'] in content
    assert form_data["body"] in content



# # # test income comment validation
@pytest.mark.django_db
def test_income_comment(create_income, auto_login_user):
    income, client, user = create_income

    url = reverse('wallet:income_comment', kwargs= {
        'income_id': income.id
    })

    form_data = {
        'name': '',
        'email': 'john@e@',
        'body': ''
    }

    response = client.post(url, data=form_data)
    content = response.content.decode('utf-8')

    assert 'This field is required' in content
    assert 'Enter a valid email address' in content



# # # test income share
@pytest.mark.django_db
def test_income_share(create_income):
    income, client, user = create_income

    url = reverse('wallet:income_share', kwargs={
        'income_id': income.id
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
    assert sent_email.subject == f"John Doe recommends you to look at {income.amount}"
    print(sent_email.body)
    assert sent_email.body == f"Look at {income.amount} at http://testserver{income.get_detail_url()}\n\nJohn Doe's comments: Check this out!"
