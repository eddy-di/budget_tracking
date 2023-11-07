# Generated by Django 4.1.13 on 2023-11-07 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0005_alter_spending_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='income',
            name='slug',
            field=models.SlugField(max_length=150, null=True, unique_for_date='created_at'),
        ),
    ]
