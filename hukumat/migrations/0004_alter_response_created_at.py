# Generated by Django 4.1.5 on 2023-01-18 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hukumat', '0003_response_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='response',
            name='created_at',
            field=models.DateTimeField(auto_created=True, auto_now_add=True),
        ),
    ]
