# Generated by Django 3.1.2 on 2020-11-25 04:53

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teams', '0013_auto_20201105_1820'),
        ('dashboard', '0007_auto_20201120_1308'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventPoster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='name event')),
                ('date_start', models.DateField(verbose_name='Date start event')),
                ('date_end', models.DateField(verbose_name='Date end event')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('athletes', models.ManyToManyField(blank=True, related_name='event_poster_athletes', to=settings.AUTH_USER_MODEL, verbose_name='Athletes events')),
                ('team', models.ManyToManyField(blank=True, to='teams.Team', verbose_name='Teams event')),
            ],
            options={
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
            },
        ),
    ]