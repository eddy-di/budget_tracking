from django.contrib import admin

from .models.expense import Expense
from .models.income import Income
from .models.category import Category
from .models.wallet import Wallet
from .models.sub_category import SubCategory
from .models.comment_income import IncomeComment
from .models.comment_expense import ExpenseComment
# Register your models here.


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['amount', 'currency', 'created_at', 'sub_category', 'member', 'slug', 'comment']
    list_filter = ['amount', 'created_at', 'sub_category', 'member']
    search_fields = ['amount', 'created_at', 'comment']
    prepopulated_fields = {'slug': ('currency', 'amount', 'sub_category', 'wallet')}
    raw_id_fields = ['member']
    date_hierarchy = 'created_at'
    ordering = ['created_at', 'currency']


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ['amount', 'currency', 'created_at', 'sub_category', 'member', 'slug', 'comment']
    list_filter = ['amount', 'created_at', 'sub_category', 'member']
    search_fields = ['amount', 'created_at', 'comment']
    prepopulated_fields = {'slug': ('currency', 'amount', 'sub_category', 'wallet')}
    raw_id_fields = ['member']
    date_hierarchy = 'created_at'
    ordering = ['created_at', 'currency']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']
    ordering = ['name']


@admin.register(Wallet)
class WaletAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']
    ordering = ['name']
    filter_horizontal = ['user']


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_filter = ['name', 'category']
    search_fields = ['name', 'category']
    ordering = ['name', 'category']


@admin.register(ExpenseComment)
class ExpenseCommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'expense', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']


@admin.register(IncomeComment)
class IncomeCommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'income', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']