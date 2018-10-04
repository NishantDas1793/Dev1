# Generated by Django 2.1.1 on 2018-09-18 08:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='Zip_code',
            field=models.CharField(max_length=6, validators=[django.core.validators.RegexValidator('^\\d{ 6 }$')]),
        ),
    ]