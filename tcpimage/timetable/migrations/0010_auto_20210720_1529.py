# Generated by Django 3.0.2 on 2021-07-20 12:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0009_chkboxcourse'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='br',
            name='rubric',
        ),
        migrations.DeleteModel(
            name='BrightTable',
        ),
        migrations.DeleteModel(
            name='Image',
        ),
        migrations.DeleteModel(
            name='Br',
        ),
        migrations.DeleteModel(
            name='Rubric',
        ),
    ]
