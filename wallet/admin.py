from django.contrib import admin

from .models.spending import Spending
from .models.income import Income
from .models.category import Category
from .models.wallet import Wallet
from .models.sub_category import SubCategory
# Register your models here.


@admin.register(Spending)
class SpendingAdmin(admin.ModelAdmin):
    list_display = ['amount', 'currency', 'created_at', 'sub_category', 'member']
    list_filter = ['amount', 'created_at', 'sub_category', 'member']
    search_fields = ['amount', 'created_at']
    prepopulated_fields = {'slug': ('currency', 'amount', 'sub_category', 'wallet')}
    raw_id_fields = ['member']
    date_hierarchy = 'created_at'
    ordering = ['created_at']


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ['amount', 'currency', 'created_at', 'sub_category', 'member']
    list_filter = ['amount', 'created_at', 'sub_category', 'member']
    search_fields = ['amount', 'created_at']
    prepopulated_fields = {'slug': ('currency', 'amount', 'sub_category', 'wallet')}
    raw_id_fields = ['member']
    date_hierarchy = 'created_at'
    ordering = ['created_at']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name']
    list_filter = ['category_name']
    search_fields = ['category_name']
    ordering = ['category_name']


@admin.register(Wallet)
class WaletAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']
    ordering = ['name']


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['sub_category_name', 'category_name']
    list_filter = ['sub_category_name', 'category_name']
    search_fields = ['sub_category_name', 'category_name']
    ordering = ['sub_category_name', 'category_name']