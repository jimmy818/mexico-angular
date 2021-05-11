# Generated by Django 3.1.2 on 2021-03-29 17:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0013_auto_20201105_1820'),
        ('catalog', '0081_remove_block_teams'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='program',
            name='teams',
        ),
        migrations.AddField(
            model_name='program',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='teams.team', verbose_name='Assigned team'),
        ),
    ]
