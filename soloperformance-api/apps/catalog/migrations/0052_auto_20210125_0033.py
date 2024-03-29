# Generated by Django 3.1.2 on 2021-01-25 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0051_blockexercisecatalogsubparameter_choiceblockexercisecatalogsubparameter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blockexercisecatalogsubparameter',
            name='type',
            field=models.IntegerField(choices=[(1, 'Numeric'), (2, 'Numeric Catalogs'), (7, 'Percentage Catalogs'), (3, 'Time'), (4, 'Choice'), (5, 'Percentaje'), (6, 'Character of effort'), (6, 'Character of effort')], default=1, verbose_name='type'),
        ),
    ]
