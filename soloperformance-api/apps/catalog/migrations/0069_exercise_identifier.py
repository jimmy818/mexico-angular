# Generated by Django 3.1.2 on 2021-02-17 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0068_auto_20210216_1716'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercise',
            name='identifier',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Name english'),
        ),
    ]
