# Generated by Django 3.1.2 on 2021-03-01 08:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0070_auto_20210225_1204'),
        ('coach', '0009_auto_20210225_0849'),
    ]

    operations = [
        migrations.AddField(
            model_name='categoryselectionniveluser',
            name='equip',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='equip_user', to='catalog.subcategory', verbose_name='Related equipment'),
        ),
    ]
