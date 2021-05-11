# Generated by Django 3.1.2 on 2021-04-05 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0083_auto_20210329_1656'),
        ('help_coach', '0006_programworkouts'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='regionscategorycoach',
            name='regions',
        ),
        migrations.AddField(
            model_name='regionscategorycoach',
            name='regions',
            field=models.ManyToManyField(blank=True, related_name='regions_category_coach', to='catalog.SubCategory', verbose_name='regions'),
        ),
    ]