# Generated by Django 3.1.2 on 2020-10-29 04:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('security', '0012_auto_20201027_2346'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='subscription_active',
        ),
    ]
