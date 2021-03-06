# Generated by Django 3.0.2 on 2020-08-05 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0008_auto_20200805_1531'),
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teacher_name', models.CharField(blank=True, max_length=80, null=True)),
                ('teacher_class', models.CharField(blank=True, max_length=80, null=True)),
                ('teacher_mobile', models.IntegerField(blank=True, null=True)),
                ('teacher_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('teacher_landline', models.IntegerField(blank=True, null=True)),
                ('teacher_about_me', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
