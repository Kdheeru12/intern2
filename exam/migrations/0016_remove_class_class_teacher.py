# Generated by Django 3.0.2 on 2020-08-06 12:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0015_students'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='class',
            name='Class_teacher',
        ),
    ]
