# Generated by Django 4.1.5 on 2023-01-27 06:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hukumat', '0006_response_is_kech'),
    ]

    operations = [
        migrations.RenameField(
            model_name='response',
            old_name='is_kech',
            new_name='is_late',
        ),
    ]
