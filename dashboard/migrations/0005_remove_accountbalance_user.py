# Generated by Django 4.2.4 on 2024-02-29 10:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_accountbalance_user_transaction_receiver_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accountbalance',
            name='user',
        ),
    ]
