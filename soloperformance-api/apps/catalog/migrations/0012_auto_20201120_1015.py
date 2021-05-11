# Generated by Django 3.1.2 on 2020-11-20 16:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0011_phase_program'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phase',
            name='program',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='program_phase', to='catalog.program', verbose_name='Program phase'),
        ),
        migrations.AlterField(
            model_name='program',
            name='end_date',
            field=models.DateField(blank=True, null=True, verbose_name='End date'),
        ),
        migrations.AlterField(
            model_name='program',
            name='start_date',
            field=models.DateField(blank=True, null=True, verbose_name='Start date'),
        ),
    ]