# Generated by Django 3.1.2 on 2020-11-06 02:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0006_remove_exercise_institution'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='exercise_updated_by_user', to=settings.AUTH_USER_MODEL, verbose_name='Institution excercice'),
        ),
    ]
