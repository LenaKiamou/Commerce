# Generated by Django 3.2.8 on 2022-02-15 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_alter_listing_watchlist_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='current_bid',
            field=models.FloatField(blank=True, null=True),
        ),
    ]