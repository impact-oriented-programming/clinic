# Generated by Django 3.0.5 on 2020-04-26 17:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='session',
            name='doctor',
        ),
    ]
