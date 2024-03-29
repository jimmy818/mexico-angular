# Generated by Django 3.1.2 on 2020-12-02 23:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0028_auto_20201202_1735'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='day',
            name='date',
        ),
        migrations.RemoveField(
            model_name='day',
            name='request_library',
        ),
        migrations.AlterField(
            model_name='day',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='day_created_by_user', to=settings.AUTH_USER_MODEL, verbose_name='created_by day'),
        ),
        migrations.AlterField(
            model_name='day',
            name='has_library',
            field=models.BooleanField(default=False, verbose_name='has_library'),
        ),
        migrations.AlterField(
            model_name='day',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='day_updated_by_user', to=settings.AUTH_USER_MODEL, verbose_name='updated_by day'),
        ),
    ]
