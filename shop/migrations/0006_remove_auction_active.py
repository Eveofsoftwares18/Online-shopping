# Generated by Django 3.2.3 on 2021-05-26 18:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auction_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auction',
            name='active',
        ),
    ]