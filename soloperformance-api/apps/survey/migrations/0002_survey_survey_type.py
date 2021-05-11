# Generated by Django 3.1.2 on 2021-01-20 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='survey_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'pre-training'), (2, 'post-training')], default=1),
        ),
    ]