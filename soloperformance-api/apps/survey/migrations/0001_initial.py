# Generated by Django 3.1.2 on 2021-01-20 06:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desciption', models.CharField(blank=True, max_length=250, null=True)),
                ('name', models.CharField(max_length=250)),
            ],
            options={
                'verbose_name': 'Survey',
                'verbose_name_plural': 'Survey',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('required', models.BooleanField(default=True)),
                ('text', models.TextField()),
                ('question_type', models.PositiveSmallIntegerField(choices=[(1, 'text'), (3, 'integer'), (2, 'time')], default=1)),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.survey')),
            ],
            options={
                'verbose_name': 'Question',
                'verbose_name_plural': 'Questions',
            },
        ),
    ]