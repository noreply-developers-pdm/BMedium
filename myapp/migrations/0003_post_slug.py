# Generated by Django 2.2.4 on 2019-08-16 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_auto_20190811_1345'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(default='default-slug', max_length=140, unique=True),
        ),
    ]
