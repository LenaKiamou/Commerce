# Generated by Django 3.2.8 on 2022-02-12 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bids',
            name='value_offer',
            field=models.FloatField(default=None),
        ),
    ]
