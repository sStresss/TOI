# Generated by Django 3.0.2 on 2020-12-25 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0004_brighttable'),
    ]

    operations = [
        migrations.CreateModel(
            name='CrudUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TimeField(blank=True, max_length=30)),
                ('address', models.IntegerField(blank=True, max_length=100)),
            ],
        ),
    ]
