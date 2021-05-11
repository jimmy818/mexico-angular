# Generated by Django 3.1.2 on 2020-10-15 16:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('regions', '0001_initial'),
        ('security', '0003_user_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='regions.region', verbose_name='Region user'),
        ),
    ]