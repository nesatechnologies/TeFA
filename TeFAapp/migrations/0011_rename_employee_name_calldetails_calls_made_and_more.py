# Generated by Django 4.2.10 on 2024-02-26 08:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TeFAapp', '0010_alter_calldetails_employee_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='calldetails',
            old_name='employee_name',
            new_name='calls_made',
        ),
        migrations.RenameField(
            model_name='calldetails',
            old_name='updated_by',
            new_name='calls_updated',
        ),
    ]
