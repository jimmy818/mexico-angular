# Generated by Django 3.1.2 on 2021-03-29 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coach', '0014_nivel_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nivel',
            name='description',
            field=models.CharField(default='', max_length=500, verbose_name='Description'),
            preserve_default=False,
        ),
    ]