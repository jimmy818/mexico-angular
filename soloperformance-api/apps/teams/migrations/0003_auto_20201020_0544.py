# Generated by Django 3.1.2 on 2020-10-20 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0002_institution'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institution',
            name='active',
            field=models.BooleanField(default=False, verbose_name='institution active'),
        ),
    ]
