# Generated by Django 4.2.4 on 2023-10-14 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_accountbalance_transaction_history'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deposit', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('transfer', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('new_balance', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
        ),
        migrations.RemoveField(
            model_name='accountbalance',
            name='transaction_history',
        ),
        migrations.AddField(
            model_name='accountbalance',
            name='transactions',
            field=models.ManyToManyField(to='dashboard.transaction'),
        ),
    ]
