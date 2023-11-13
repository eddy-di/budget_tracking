# Generated by Django 4.1.13 on 2023-11-09 08:45

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
        ('wallet', '0007_spendingcomment_incomecomment_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='spending',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
