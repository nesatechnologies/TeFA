import datetime

from django.db import models
from django.core.validators import RegexValidator


alphanumeric = RegexValidator(r'^[0-9a-zA-Z\-]*$', 'Only alphanumeric characters are allowed.')

# Create your models here.
class Lead(models.Model):
    control_no = models.IntegerField()
    date_time_added = models.DateField(("Date"), default=datetime.date.today)
    lead_given_date = models.DateField()
    lead_no = models.CharField(max_length=10, blank=True, null=True, validators=[alphanumeric])
    name = models.CharField(max_length= 50)
    course = models.CharField(max_length=50)
    phone_no = models.IntegerField()
    email = models.EmailField(max_length=30)
    place = models.CharField(max_length=50)
    remark = models.CharField(max_length=250)
    status = models.IntegerField(default=0)
    def __str__(self):
        return '{}'.format(self.control_no)

class Calldetails(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    employee_name = models.CharField(max_length=50)
    emp_remark = models.CharField(max_length=250)
    called_datetime = models.DateField(("Date"), default=datetime.date.today)
    called_meadium = models.CharField(max_length=10)
    updated_by = models.CharField(max_length=50,default='')

    def __str__(self):
        return '{} - {} - {}'.format(self.lead.control_no, self.lead.status, self.updated_by)

class Folloup(models.Model):
    call_detail = models.ForeignKey(Calldetails, on_delete=models.CASCADE)
    control_no = models.IntegerField()
    remark = models.CharField(max_length=250)

    def __str__(self):
        return '{}'.format(self.control_no)


class Employee_details(models.Model):
    user_name = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    emp_id = models.CharField(max_length=10)
    def __str__(self):
        return '{} - {} '.format(self.emp_id, self.name)

