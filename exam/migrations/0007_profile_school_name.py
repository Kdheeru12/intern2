# Generated by Django 3.0.2 on 2020-08-05 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0006_auto_20200805_1517'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='school_name',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
