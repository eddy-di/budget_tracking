from django.db import models

from .sub_category import SubCategory
from .wallet import Wallet
from django.contrib.auth.models import User


class Spending(models.Model):
    class CurrencyChoices(models.IntegerChoices): # this subclass represents Python enum in Django
        # in shell is you type from wallet.models.spending import Spending and then
        # Spending.CurrencyChoices.choices stores -> [(1, 'KGS'), (2, 'USD'), (3, 'RUB'), (4, 'KZT'), (5, 'EUR'), (6, 'GBP'), (7, 'CNY'), (8, 'TRY')] 
        # Spending.CurrencyChoices.labels -> ['KGS', 'USD', 'RUB', 'KZT', 'EUR', 'GBP', 'CNY', 'TRY'] 
        # Spending.CurrencyChoices.values -> [1, 2, 3, 4, 5, 6, 7, 8] 
        # Spending.CurrencyChoices.names -> ['KGS', 'USD', 'RUB', 'KZT', 'EUR', 'GBP', 'CNY', 'TRY'] 
        # if [currency = "KGS = 1, 'KGS'"] as in str, name = currency[0:3], values = currency[6:7], labels = currency[-4:-1]
        KGS = 1, 'KGS'
        USD = 2, 'USD'
        RUB = 3, 'RUB'
        KZT = 4, 'KZT'
        EUR = 5, 'EUR'
        GBP = 6, 'GBP'
        CNY = 7, 'CNY'
        TRY = 8, 'TRY'

    amount = models.DecimalField(decimal_places=2, max_digits=12)
    currency = models.PositiveSmallIntegerField(
        choices=CurrencyChoices.choices, 
        default=CurrencyChoices.KGS
    )
    created_at = models.DateTimeField(auto_now_add=True)
    sub_category = models.ForeignKey(SubCategory, 
                                     on_delete=models.CASCADE, 
                                     null=True)
    wallet = models.ForeignKey(Wallet, 
                               on_delete=models.CASCADE, 
                               null=True)
    member = models.ForeignKey(User, 
                               on_delete=models.CASCADE,
                               related_name='wallet_spendings')

    class Meta:
        # атрибут ordering, сообщает Django, что он должен сортировать результаты по полю creted_at 
        # дефис указывает на обратный хронологический порядок (от нового к старому), 
        # указанный порядок будет применяться для запросов к базе данных
        ordering = ['-created_at']
        # опция indexes позволяет определять в модели индексы базы данных, которые могут содержать одно 
        # или несколько полей в возрастающем либо убывающем порядке, или функциональные выражения и функции базы данных.
        indexes = [
            models.Index(fields=['-created_at'])
            ]
        
    def __str__(self):
        return f'{self.amount} {self.currency} - {self.created_at}'