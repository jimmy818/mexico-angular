# Generated by Django 3.1.2 on 2020-11-05 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subcategory',
            name='code',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Subcategory name'),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='level',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Level of subcategory'),
        ),
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('english_name', models.CharField(max_length=250, verbose_name='Name english')),
                ('spanish_name', models.CharField(max_length=250, verbose_name='Name spanish')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True, verbose_name='subcategory active')),
                ('sub_category', models.ManyToManyField(to='catalog.SubCategory', verbose_name='Subcategories Exercise')),
            ],
        ),
    ]
