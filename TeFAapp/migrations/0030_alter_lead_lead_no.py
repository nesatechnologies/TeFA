# Generated by Django 4.2.2 on 2024-03-24 10:57

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TeFAapp', '0029_alter_lead_course_alter_lead_course_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='lead_no',
            field=models.CharField(blank=True, max_length=30, null=True, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z\\-]*$', 'Only alphanumeric characters are allowed.')]),
        ),
    ]
