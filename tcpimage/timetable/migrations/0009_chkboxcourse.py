# Generated by Django 3.0.2 on 2021-07-16 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0008_auto_20210715_1218'),
    ]

    operations = [
        migrations.CreateModel(
            name='chkboxcourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coursename', models.CharField(max_length=100)),
            ],
        ),
    ]
