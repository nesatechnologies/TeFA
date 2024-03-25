# Generated by Django 4.2.2 on 2024-03-24 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TeFAapp', '0028_lead_priority'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='course',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='lead',
            name='course_type',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='lead',
            name='degree',
            field=models.CharField(blank=True, default='', max_length=250),
        ),
        migrations.AlterField(
            model_name='lead',
            name='email',
            field=models.EmailField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='lead',
            name='name',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='lead',
            name='phone_no',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='lead',
            name='place',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='lead',
            name='remark',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='lead',
            name='source',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]