# Generated by Django 3.1.2 on 2020-11-23 17:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0013_day_week'),
    ]

    operations = [
        migrations.CreateModel(
            name='Workout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Workout name')),
                ('start_time', models.TimeField(blank=True, null=True, verbose_name='Start time')),
                ('end_time', models.TimeField(blank=True, null=True, verbose_name='End time')),
                ('location', models.CharField(max_length=250, verbose_name='Workout location')),
                ('active', models.BooleanField(default=True, verbose_name='Workout active')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='workout_created_by_user', to=settings.AUTH_USER_MODEL, verbose_name='Institution workout')),
                ('day', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='day_workout', to='catalog.day', verbose_name='Day workout')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='workout_updated_by_user', to=settings.AUTH_USER_MODEL, verbose_name='Institution workout')),
            ],
            options={
                'verbose_name': 'Workout',
                'verbose_name_plural': 'Workouts',
            },
        ),
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('REGULAR', 'Regular'), ('SUPERSET', 'SuperSet'), ('RFT', 'RFT'), ('EMON', 'EMON'), ('AMRAP', 'AMRAP')], default='REGULAR', max_length=250, verbose_name="Block's type")),
                ('limit', models.PositiveSmallIntegerField(verbose_name='Limit of exercises in a block')),
                ('active', models.BooleanField(default=True, verbose_name='Block active')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('athletes', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='Assigned athletes')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.category', verbose_name='Category block')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='block_created_by_user', to=settings.AUTH_USER_MODEL, verbose_name='Institution block')),
                ('exercises', models.ManyToManyField(blank=True, to='catalog.Exercise', verbose_name='Exercises block')),
                ('subcategory', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.subcategory', verbose_name='Subcategory block')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='block_updated_by_user', to=settings.AUTH_USER_MODEL, verbose_name='Institution block')),
                ('workout', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='workout_day', to='catalog.workout', verbose_name='Workout day')),
            ],
            options={
                'verbose_name': 'Block',
                'verbose_name_plural': 'Blocks',
            },
        ),
    ]