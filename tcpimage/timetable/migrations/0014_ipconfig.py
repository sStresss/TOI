# Generated by Django 3.0.2 on 2021-10-15 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0013_manualcount'),
    ]

    operations = [
        migrations.CreateModel(
            name='IpConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=16)),
                ('mask', models.CharField(max_length=16)),
                ('gateway', models.CharField(max_length=16)),
            ],
        ),
    ]
