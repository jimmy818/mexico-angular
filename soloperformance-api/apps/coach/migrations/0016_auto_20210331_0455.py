# Generated by Django 3.1.2 on 2021-03-31 10:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0083_auto_20210329_1656'),
        ('coach', '0015_auto_20210329_1644'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categoryselectionniveluser',
            name='equip',
        ),
        migrations.AlterField(
            model_name='nivel',
            name='description',
            field=models.CharField(default='Description', max_length=500, verbose_name='Description'),
        ),
        migrations.CreateModel(
            name='EquipUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='equip_user_created_by_user', to=settings.AUTH_USER_MODEL, verbose_name='created_by equip_user')),
                ('equipment', models.ManyToManyField(related_name='equip_user', to='catalog.CategoryEquipment', verbose_name='Equipment')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='equip_user_updated_by_user', to=settings.AUTH_USER_MODEL, verbose_name='updated_by equip_user')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='equip_by_user', to=settings.AUTH_USER_MODEL, verbose_name='User Related')),
            ],
            options={
                'verbose_name': 'Equipment User',
                'verbose_name_plural': 'Equipments Users',
            },
        ),
    ]