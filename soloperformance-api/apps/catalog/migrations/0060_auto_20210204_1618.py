# Generated by Django 3.1.2 on 2021-02-04 22:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0059_auto_20210204_1600'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blockexercisecatalogsubparameter',
            name='conversion_measure',
        ),
        migrations.RemoveField(
            model_name='itemexerciseblockrelatedcatalog',
            name='conversion',
        ),
        migrations.DeleteModel(
            name='ConversionMeasure',
        ),
    ]
