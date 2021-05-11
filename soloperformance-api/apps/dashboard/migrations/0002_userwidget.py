# Generated by Django 3.1.2 on 2020-10-29 22:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserWidget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveSmallIntegerField(verbose_name='order widget')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User widget')),
                ('widget', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.widget', verbose_name='Widget user')),
            ],
            options={
                'verbose_name': 'User Widget',
                'verbose_name_plural': 'Users Widget',
            },
        ),
    ]