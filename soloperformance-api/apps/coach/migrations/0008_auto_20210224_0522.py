# Generated by Django 3.1.2 on 2021-02-24 11:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coach', '0007_auto_20210224_0437'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name Category')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.AlterField(
            model_name='categoryselectionniveluser',
            name='nivel_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='nivel_user', to='coach.niveluser', verbose_name='Related nivel_user'),
        ),
        migrations.AlterField(
            model_name='categoryselection',
            name='name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category_nivel', to='coach.category', verbose_name='Related category_selection'),
        ),
    ]
