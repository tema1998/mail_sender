# Generated by Django 4.2.10 on 2024-02-16 20:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_emailhistory_remove_singleemail_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taskcore',
            name='number_of_valid_emails',
        ),
    ]
