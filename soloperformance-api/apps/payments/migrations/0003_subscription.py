# Generated by Django 3.1.2 on 2020-10-22 03:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('teams', '0003_auto_20201020_0544'),
        ('payments', '0002_auto_20201020_1502'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.PositiveSmallIntegerField(choices=[(1, 'TRIAL'), (2, 'PAYING'), (3, 'DEMOS')], default=3, verbose_name='type subscription')),
                ('ends', models.DateField(verbose_name='ends suscription')),
                ('is_active', models.BooleanField(default=True, verbose_name='active subscription')),
                ('total_athletes', models.PositiveSmallIntegerField(verbose_name='number of athletes')),
                ('total_coaches', models.PositiveSmallIntegerField(verbose_name='number of athletes')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=6, verbose_name='price payed of subscription in dollars')),
                ('institution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teams.institution', verbose_name='institution')),
            ],
            options={
                'verbose_name': 'Subscription',
                'verbose_name_plural': 'Subscriptions',
            },
        ),
    ]
