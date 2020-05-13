# Generated by Django 3.0.5 on 2020-05-13 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor_interface', '0005_diagnosis_medication'),
    ]

    operations = [
        migrations.AddField(
            model_name='medication',
            name='medication_details',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='medication',
            name='medication_package_size',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name='medication',
            name='medication_pharmasoft_code',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='medication',
            name='medication_yrpa_code',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
