# Generated by Django 3.1.2 on 2020-12-07 22:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0038_auto_20201204_0136'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workout',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='workout',
            name='updated_by',
        ),
    ]
