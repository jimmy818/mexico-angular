# Generated by Django 3.1.2 on 2020-10-22 17:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0005_remove_institution_plan_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='created_by_team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='teams.institution', verbose_name='institution created'),
        ),
    ]