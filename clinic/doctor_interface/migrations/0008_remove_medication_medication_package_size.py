# Generated by Django 3.0.5 on 2020-05-13 14:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doctor_interface', '0007_auto_20200513_1735'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medication',
            name='medication_package_size',
        ),
    ]
