# Generated by Django 4.2.10 on 2024-02-29 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TeFAapp', '0022_remove_folloup_lead'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='degree',
            field=models.CharField(default='', max_length=250),
        ),
        migrations.AddField(
            model_name='lead',
            name='source',
            field=models.CharField(default='', max_length=100),
        ),
    ]