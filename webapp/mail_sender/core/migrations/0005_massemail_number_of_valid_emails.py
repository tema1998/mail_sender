# Generated by Django 5.0.2 on 2024-02-12 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_massemail'),
    ]

    operations = [
        migrations.AddField(
            model_name='massemail',
            name='number_of_valid_emails',
            field=models.SmallIntegerField(default=0),
            preserve_default=False,
        ),
    ]
