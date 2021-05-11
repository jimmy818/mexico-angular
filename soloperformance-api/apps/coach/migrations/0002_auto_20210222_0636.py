# Generated by Django 3.1.2 on 2021-02-22 06:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('coach', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categoryselection',
            name='nivel',
        ),
        migrations.AlterField(
            model_name='categoryselection',
            name='created_by',
            field=models.ForeignKey(blank=True, default=42, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category_selection_created_by_user', to=settings.AUTH_USER_MODEL, verbose_name='created_by category_selection'),
        ),
    ]
