# Generated by Django 4.1.5 on 2023-03-30 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_remove_requestmodel_location_latitude_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestmodel',
            name='location_latitude',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='requestmodel',
            name='location_longitude',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
