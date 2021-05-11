# Generated by Django 3.1.2 on 2021-04-15 09:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('webpush', '0002_auto_20190603_0005'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PushInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='webpush_info2', to='webpush.group')),
                ('subscription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='webpush_info2', to='webpush.subscriptioninfo')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='webpush_info2', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
