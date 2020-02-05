# Generated by Django 3.0.2 on 2020-02-04 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_data', '0001_initial'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='alertregions',
            name='regions_unique_together',
        ),
        migrations.AddConstraint(
            model_name='alertregions',
            constraint=models.UniqueConstraint(fields=('geohash', 'region', 'time', 'expires'), name='regions_unique_together'),
        ),
    ]