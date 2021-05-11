# Generated by Django 3.1.2 on 2020-11-20 18:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teams', '0013_auto_20201105_1820'),
        ('dashboard', '0005_event'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='date',
        ),
        migrations.AddField(
            model_name='event',
            name='athletes',
            field=models.ManyToManyField(blank=True, related_name='event_athletes', to=settings.AUTH_USER_MODEL, verbose_name='Athletes events'),
        ),
        migrations.AddField(
            model_name='event',
            name='date_end',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Date end event'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='date_start',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Date start event'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='teams.team', verbose_name='Teams event'),
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(max_length=150, verbose_name='name event'),
        ),
    ]
