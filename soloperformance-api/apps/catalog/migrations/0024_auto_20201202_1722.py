# Generated by Django 3.1.2 on 2020-12-02 23:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0023_auto_20201202_1722'),
    ]

    operations = [
        migrations.RenameField(
            model_name='program',
            old_name='teams',
            new_name='team',
        ),
    ]