# Generated by Django 3.1.2 on 2020-12-04 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0037_auto_20201204_0134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='day',
            name='day',
            field=models.IntegerField(choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (7, 'Sunday')], default=7, verbose_name='Day name'),
        ),
    ]
