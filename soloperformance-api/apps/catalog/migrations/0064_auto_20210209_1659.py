# Generated by Django 3.1.2 on 2021-02-09 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0063_auto_20210208_1556'),
    ]

    operations = [
        migrations.RenameField(
            model_name='itemexerciseblockrelatedcatalog',
            old_name='value_extra',
            new_name='value3',
        ),
        migrations.AddField(
            model_name='itemexerciseblockrelatedcatalog',
            name='value4',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]