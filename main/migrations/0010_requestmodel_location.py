# Generated by Django 4.1.5 on 2023-02-27 16:00

from django.db import migrations
import location_field.models.plain


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_requestmodel_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestmodel',
            name='location',
            field=location_field.models.plain.PlainLocationField(blank=True, max_length=63, null=True),
        ),
    ]