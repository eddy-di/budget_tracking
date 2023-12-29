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
    print(expense.amount)

    assert response_list.status_code == 200
    assert response_detail.status_code == 200

    data = {
        'amount': fake_decimal_another
    }

    response_detail_patch = api_client.patch(detail_url, data=data)

    patched_expense = Expense.objects.get(id=expense.id)
    print(patched_expense.amount)

    assert response_detail_patch.status_code == 200
    assert expense.amount != patched_expense.amount
    assert patched_expense.amount == data['amount']

    api_client.force_authenticate(user=None)