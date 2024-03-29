# Generated by Django 3.1.2 on 2020-10-29 22:11

import apps.dashboard.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Widget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='name widget')),
                ('image', models.ImageField(upload_to=apps.dashboard.models.path_and_rename, verbose_name='image widget')),
            ],
            options={
                'verbose_name': 'Widget',
                'verbose_name_plural': 'Widgets',
            },
        ),
    ]
