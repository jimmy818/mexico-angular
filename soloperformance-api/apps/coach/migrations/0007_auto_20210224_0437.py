# Generated by Django 3.1.2 on 2021-02-24 10:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coach', '0006_auto_20210223_0759'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='workoutnivelphase',
            options={'verbose_name': 'Workout Nivel Phase', 'verbose_name_plural': 'Workout Nivel Phases'},
        ),
        migrations.AlterField(
            model_name='blocknivel',
            name='nivel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coach.nivel', verbose_name='nivel'),
        ),
        migrations.CreateModel(
            name='CategorySelectionNivelUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_selection', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category_nivel', to='coach.categoryselection', verbose_name='Related category_selection')),
                ('nivel_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='nivel_user', to='coach.categoryselection', verbose_name='Related nivel_user')),
            ],
            options={
                'verbose_name': 'Category Selection Nivel User',
                'verbose_name_plural': 'Category Selection Nivel Users',
            },
        ),
    ]
