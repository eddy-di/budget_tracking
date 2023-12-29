from decimal import Decimal
import pytest
from faker import Faker


from wallet.models.wallet import Wallet
from wallet.models.category import Category
from wallet.models.sub_category import SubCategory
from wallet.models.income import Income
from wallet.models.expense import Expense
from django.urls import reverse

fake = Faker()

fake_decimal = fake.pydecimal(3, 2, True)
fake_decimal_another = fake.pydecimal(4, 2, True)


@pytest.mark.django_db
def test_expense_views_get(api_client, create_user):
    user = create_user()
    api_client.force_authenticate(user=user)
    cat = Category.objects.create(name='utilities')
    subcat = SubCategory.objects.create(name='electricity', category=cat)
    wallet = Wallet.objects.create(name=fake.word())
    wallet.users.set([user.id])
    comment_inst = fake.text()
    price_amount = fake_decimal

    expense = Expense.objects.create(
        amount = price_amount, 
        category = cat, 
        sub_category = subcat,
        wallet = wallet,
        member = user,
        comment = comment_inst
    )
    list_url = reverse('wallet-api:expense_list')
    detail_url = reverse('wallet-api:expense_detail', args=[expense.id])

    response_list = api_client.get(list_url)
    response_detail = api_client.get(detail_url)

    assert response_list.status_code == 200
    assert response_detail.status_code == 200

    data = {
        'amount': price_amount,
        'category': cat.id,
        'sub_category': subcat.id,
        'wallet': wallet.id,
        'member': user.id,
        'comment': comment_inst
    }

    response = api_client.post(list_url, data=data)
    print(response.data)

    assert response.status_code == 201
    assert response.data['amount'] == price_amount
    assert response.data['category'] == cat.id
    assert response.data['sub_category'] == subcat.id
    assert response.data['wallet'] == wallet.id
    assert response.data['member'] == user.username
    assert response.data['comment'] == comment_inst

    api_client.force_authenticate(user=None)