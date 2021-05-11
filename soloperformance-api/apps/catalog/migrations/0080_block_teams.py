# Generated by Django 3.1.2 on 2021-03-26 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0013_auto_20201105_1820'),
        ('catalog', '0079_auto_20210323_0945'),
    ]

    operations = [
        migrations.AddField(
            model_name='block',
            name='teams',
            field=models.ManyToManyField(blank=True, to='teams.Team', verbose_name='Assigned athletes'),
        ),
    ]
