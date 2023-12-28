import pytest

from wallet.models.wallet import Wallet
from wallet.models.category import Category
from wallet.models.sub_category import SubCategory

from faker import Faker
from django.urls import reverse


fake = Faker()

fake_decimal = fake.pydecimal(3, 2, True)

# required_fields = ['amount', 'category', 'sub_category', 'wallet'] 

@pytest.mark.django_db
def test_income_create_api(api_client, create_user):
    user = create_user()
    api_client.force_authenticate(user=user)
    cat = Category.objects.create(name='income')
    subcat = SubCategory.objects.create(name='Salary', category=cat)
    wallet = Wallet.objects.create(name=fake.word())
    wallet.users.set([user.id])
    comment = fake.text()

    url = reverse('wallet-api:income_list')
    data = {
        'amount': fake_decimal,
        'category': cat.id,
        'sub_category': subcat.id,
        'wallet': wallet.id,
        'member': user.id,
        'comment': comment
    }

    response = api_client.post(url, data=data)
    print(response.data)

    assert response.status_code == 201
    assert response.data['amount'] == fake_decimal
    assert response.data['category'] == cat.id
    assert response.data['sub_category'] == subcat.id
    assert response.data['wallet'] == wallet.id
    assert response.data['member'] == user.username
    assert response.data['comment'] == comment

    api_client.force_authenticate(user=None)