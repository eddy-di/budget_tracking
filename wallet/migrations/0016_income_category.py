# Generated by Django 4.1.13 on 2023-12-10 06:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0015_rename_category_name_subcategory_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='income',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='wallet.category'),
        ),
    ]
