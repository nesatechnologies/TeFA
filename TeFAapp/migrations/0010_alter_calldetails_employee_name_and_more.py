# Generated by Django 4.2.10 on 2024-02-26 07:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TeFAapp', '0009_alter_employee_details_emp_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calldetails',
            name='employee_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='calls_made', to='TeFAapp.employee_details'),
        ),
        migrations.AlterField(
            model_name='calldetails',
            name='updated_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='calls_updated', to='TeFAapp.employee_details'),
        ),
    ]
