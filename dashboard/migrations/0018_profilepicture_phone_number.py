# Generated by Django 4.2.4 on 2024-08-06 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0017_alter_profilepicture_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='profilepicture',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
