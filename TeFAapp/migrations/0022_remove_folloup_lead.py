# Generated by Django 4.2.10 on 2024-02-27 09:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TeFAapp', '0021_folloup_called_datetime_folloup_called_meadium_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='folloup',
            name='lead',
        ),
    ]
