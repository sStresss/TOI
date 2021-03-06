# Generated by Django 3.0.2 on 2020-11-18 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0003_mainpage'),
    ]

    operations = [
        migrations.CreateModel(
            name='BrightTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField(max_length=50, verbose_name='Время')),
                ('bright', models.PositiveIntegerField(max_length=50, verbose_name='Яркость')),
                ('enable', models.BooleanField(verbose_name='Состояние')),
                ('published', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликованно')),
            ],
        ),
    ]
