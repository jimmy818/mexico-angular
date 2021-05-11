# Generated by Django 3.1.2 on 2021-02-16 23:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0067_itemexerciseblockrelatedcatalog_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itemexerciseblockrelatedcatalog',
            name='type',
        ),
        migrations.CreateModel(
            name='RowBlockType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row', models.PositiveSmallIntegerField()),
                ('type', models.PositiveSmallIntegerField(choices=[(1, 'Warm Up'), (2, 'Failure'), (3, 'Drops set')], default=1, verbose_name='type')),
                ('exercise_block', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.exerciseblock')),
            ],
            options={
                'verbose_name': 'Row Block Type',
                'verbose_name_plural': 'Rows Block Type',
                'ordering': ('row',),
                'unique_together': {('exercise_block', 'row')},
            },
        ),
    ]