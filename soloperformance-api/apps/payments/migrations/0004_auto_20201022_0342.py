# Generated by Django 3.1.2 on 2020-10-22 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0003_subscription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='total_coaches',
            field=models.PositiveSmallIntegerField(verbose_name='number of coaches'),
        ),
    ]