# Generated by Django 4.2.10 on 2024-03-07 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TeFAapp', '0024_courses'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='course_type',
            field=models.CharField(default='not mentioned', max_length=20),
        ),
    ]