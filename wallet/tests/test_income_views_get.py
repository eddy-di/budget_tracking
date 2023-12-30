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
def test_income_views_get(api_client, create_user):
    user = create_user()
    api_client.force_authenticate(user=user)
    cat = Category.objects.create(name='utilities')
    subcat = SubCategory.objects.create(name='electricity', category=cat)
    wallet = Wallet.objects.create(name=fake.word())
    wallet.users.set([user.id])
    comment_inst = fake.text()
    price_amount = fake_decimal

    income = Income.objects.create(
        amount = price_amount, 
        category = cat, 
        sub_category = subcat,
        wallet = wallet,
        member = user,
        comment = comment_inst
    )
    list_url = reverse('wallet-api:income_list')
    detail_url = reverse('wallet-api:income_detail', args=[income.id])

    response_list = api_client.get(list_url)
    response_detail = api_client.get(detail_url)

    assert response_list.status_code == 200
    assert response_detail.status_code == 200
    

    api_client.force_authenticate(user=None)