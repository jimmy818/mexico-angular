# Generated by Django 3.1.2 on 2021-03-29 15:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0080_block_teams'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='block',
            name='teams',
        ),
    ]
