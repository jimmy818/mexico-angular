# Generated by Django 3.1.2 on 2020-12-03 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0033_week_number_week'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='block',
            name='mins',
        ),
        migrations.RemoveField(
            model_name='block',
            name='rounds',
        ),
        migrations.RemoveField(
            model_name='exerciseblock',
            name='reps',
        ),
        migrations.RemoveField(
            model_name='exerciseblock',
            name='request_library',
        ),
        migrations.AddField(
            model_name='block',
            name='name',
            field=models.CharField(default='', max_length=250, verbose_name='Block name'),
        ),
    ]
