# Generated by Django 3.0.5 on 2020-06-03 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor_interface', '0015_auto_20200603_0914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='prescriptions',
            field=models.ManyToManyField(blank=True, related_name='prescriptions', to='doctor_interface.Medication'),
        ),
    ]