# Generated by Django 5.0.2 on 2024-02-12 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_singleemail_delete_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='singleemail',
            name='subject',
            field=models.CharField(default='subj', max_length=30),
            preserve_default=False,
        ),
    ]
