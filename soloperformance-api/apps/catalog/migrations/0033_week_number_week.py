# Generated by Django 3.1.2 on 2020-12-03 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0032_auto_20201202_1750'),
    ]

    operations = [
        migrations.AddField(
            model_name='week',
            name='number_week',
            field=models.IntegerField(blank=True, null=True, verbose_name='number week'),
        ),
    ]