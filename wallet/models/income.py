from django.db import models
from django.db.models.query import QuerySet
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import MinValueValidator
from decimal import Decimal

from .sub_category import SubCategory
from .wallet import Wallet
from .category import Category
from django.contrib.auth.models import User
from taggit.managers import TaggableManager


class IncomeManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(currency=Income.CurrencyChoices.KGS)
    
    def get_filtered(self, wallet_id, date_from, date_to):
        qs = self.filter(wallet=wallet_id)
        if date_from and date_to:
            qs = qs.filter(created_at__range=(date_from, date_to))
        return qs


class Income(models.Model):
    class CurrencyChoices(models.IntegerChoices):# this subclass represents Python enum in Django
        # in shell is you type from wallet.models.expense import Expense and then
        # Expense.CurrencyChoices.choices stores -> [(1, 'KGS'), (2, 'USD'), (3, 'RUB'), (4, 'KZT'), (5, 'EUR'), (6, 'GBP'), (7, 'CNY'), (8, 'TRY')] 
        # Expense.CurrencyChoices.labels -> ['KGS', 'USD', 'RUB', 'KZT', 'EUR', 'GBP', 'CNY', 'TRY'] 
        # Expense.CurrencyChoices.values -> [1, 2, 3, 4, 5, 6, 7, 8] 
        # Expense.CurrencyChoices.names -> ['KGS', 'USD', 'RUB', 'KZT', 'EUR', 'GBP', 'CNY', 'TRY'] 
        # if [currency = "KGS = 1, 'KGS'"] as in str, name = currency[0:3], values = currency[6:7], labels = currency[-4:-1]
        KGS = 1, 'KGS'
        USD = 2, 'USD'
        RUB = 3, 'RUB'
        KZT = 4, 'KZT'
        EUR = 5, 'EUR'
        GBP = 6, 'GBP'
        CNY = 7, 'CNY'
        TRY = 8, 'TRY'

    amount = models.DecimalField(decimal_places=2, max_digits=12, 
                                 validators=[MinValueValidator(Decimal('0.00'))])
    comment = models.TextField(null=True, blank=True) # part where the text for the expense or income can be provided if necessary
    currency = models.PositiveSmallIntegerField(
        choices=CurrencyChoices.choices, 
        default=CurrencyChoices.KGS
    )
    slug = models.SlugField(max_length=150,
                            null=True,
                            unique_for_date='created_at')
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, 
                                 on_delete=models.CASCADE, 
                                 null=True)
    sub_category = models.ForeignKey(SubCategory, 
                                     on_delete=models.CASCADE, 
                                     null=True)
    wallet = models.ForeignKey(Wallet, 
                               on_delete=models.CASCADE, 
                               null=True)
    member = models.ForeignKey(User, 
                               on_delete=models.CASCADE,
                               related_name='wallet_incomes')
    
    objects = IncomeManager()

    tags = TaggableManager()

    class Meta:
        # атрибут ordering, сообщает Django, что он должен сортировать результаты по полю creted_at 
        # дефис указывает на обратный хронологический порядок (от нового к старому), 
        # указанный порядок будет применяться для запросов к базе данных
        ordering = ['-created_at']
        # Указанная опция позволяет определять в модели индексы базы данных, которые могут содержать одно 
        # или несколько полей в возрастающем либо убывающем порядке, или функциональные выражения и функции базы данных.
        indexes = [
            models.Index(fields=['-created_at'])
            ]
        
        
    def __str__(self):
        return f'("id":{self.id}\n"amount*":{self.amount}\n"currency":{self.currency}\n"created_at":{self.created_at}\n"category*":{self.category}\n"sub_category*":{self.sub_category}\n"wallet*":{self.wallet}\n"comment*":{self.comment})'
    
    
    def get_detail_url(self):
        return reverse('wallet:income_detail',
                       args=[self.wallet_id, 
                             self.id])
    

    def save(self, *args, **kwargs):
        slug_str = f'{self.currency}-{self.amount}-{self.sub_category.id}-{self.wallet.id}'
        self.slug = slugify(slug_str)
        super(Income, self).save(*args, **kwargs)