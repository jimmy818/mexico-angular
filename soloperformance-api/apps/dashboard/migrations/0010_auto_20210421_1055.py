# Generated by Django 3.1.7 on 2021-04-21 15:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_auto_20201203_2353'),
    ]

    operations = [
        migrations.AddField(
            model_name='userwidget',
            name='size',
            field=models.IntegerField(default=12, validators=[django.core.validators.MaxValueValidator(12), django.core.validators.MinValueValidator(1)], verbose_name='Size'),
        ),
        migrations.AddField(
            model_name='widget',
            name='resizable',
            field=models.BooleanField(default=True, verbose_name='Resizable'),
        ),
    ]