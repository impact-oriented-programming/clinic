# Generated by Django 3.0.5 on 2020-05-24 13:35

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('reception_desk', '0007_auto_20200524_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctorslot',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]