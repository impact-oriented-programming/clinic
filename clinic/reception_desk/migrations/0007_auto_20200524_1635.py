# Generated by Django 3.0.5 on 2020-05-24 13:35

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('reception_desk', '0006_auto_20200524_1634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctorslot',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 5, 24, 13, 35, 26, 546914, tzinfo=utc)),
        ),
    ]