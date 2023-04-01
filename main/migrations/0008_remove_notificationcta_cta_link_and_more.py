# Generated by Django 4.1.5 on 2023-01-20 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_notificationcta'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notificationcta',
            name='cta_link',
        ),
        migrations.AddField(
            model_name='notificationcta',
            name='request_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
