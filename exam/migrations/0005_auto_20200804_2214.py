# Generated by Django 3.0.2 on 2020-08-04 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0004_auto_20200804_2112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.EmailField(default=1, max_length=254, unique=True),
            preserve_default=False,
        ),
    ]
