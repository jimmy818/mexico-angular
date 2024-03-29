# Generated by Django 3.1.2 on 2020-12-01 06:52

import apps.catalog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0018_auto_20201126_1051'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coding',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name category')),
                ('icon', models.ImageField(upload_to=apps.catalog.models.path_and_rename_icon, verbose_name='icon category')),
            ],
            options={
                'verbose_name': 'Category Workout',
                'verbose_name_plural': 'Categories Workouts',
            },
        ),
    ]
