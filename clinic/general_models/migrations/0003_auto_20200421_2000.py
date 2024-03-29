# Generated by Django 3.0.5 on 2020-04-21 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general_models', '0002_auto_20200419_1938'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='license_number',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='patient',
            name='date_of_birth',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='origin_country',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
