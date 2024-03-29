# Generated by Django 3.1.2 on 2021-01-25 06:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0050_auto_20210124_2346'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlockExerciseCatalogSubparameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Title')),
                ('type', models.IntegerField(choices=[(1, 'Numeric'), (2, 'Catalog'), (3, 'Time'), (4, 'Choice'), (5, 'Percentaje'), (6, 'Character of effort')], default=1, verbose_name='type')),
                ('block_exercise_catalog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.blockexercisecatalog')),
            ],
            options={
                'verbose_name': 'Block Exercise Catalog Subparameter',
                'verbose_name_plural': 'Block Exercise Catalog Subparameters',
            },
        ),
        migrations.CreateModel(
            name='ChoiceBlockExerciseCatalogSubparameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Title')),
                ('order', models.IntegerField(default=1)),
                ('block_exercise_catalog_sub_parameter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.blockexercisecatalogsubparameter')),
            ],
            options={
                'verbose_name': 'Choice Block Exercise Catalog Subparameter',
                'verbose_name_plural': 'Choices Block Exercise Catalog Subparameters',
            },
        ),
    ]
