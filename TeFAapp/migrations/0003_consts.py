# Generated by Django 4.2.10 on 2024-02-22 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TeFAapp', '0002_calldetails_updated_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='Consts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contr_no', models.IntegerField()),
            ],
        ),
    ]
