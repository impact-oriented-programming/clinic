# Generated by Django 3.0.5 on 2020-05-10 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor_interface', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='chief_complaint',
            field=models.TextField(blank=True, max_length=30, null=True),
        ),
        migrations.DeleteModel(
            name='Vitals',
        ),
    ]
