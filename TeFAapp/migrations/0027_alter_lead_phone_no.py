# Generated by Django 4.2.2 on 2024-03-20 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TeFAapp', '0026_alter_lead_course_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='phone_no',
            field=models.CharField(default='', max_length=50),
        ),
    ]
