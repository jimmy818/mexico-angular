# Generated by Django 3.1.2 on 2021-04-08 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0083_auto_20210329_1656'),
    ]

    operations = [
        migrations.AddField(
            model_name='workout',
            name='order',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]
