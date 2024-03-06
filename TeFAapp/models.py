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
    source = models.CharField(max_length=100, default='')
    degree = models.CharField(max_length=250, default='')
    def __str__(self):
        return '{}'.format(self.control_no)

class Employee_details(models.Model):
    user_name = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    emp_id = models.CharField(max_length=10)
    def __str__(self):
        return '{} - {} '.format(self.emp_id, self.name)

class Calldetails(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    calls_made = models.ForeignKey(Employee_details, on_delete=models.CASCADE, related_name='calls_made')
    emp_remark = models.CharField(max_length=250)
    called_datetime = models.DateField(("Date"), default=datetime.date.today)
    called_meadium = models.CharField(max_length=10)
    calls_updated = models.ForeignKey(Employee_details, on_delete=models.CASCADE, related_name='calls_updated')
    no_of_followups = models.IntegerField(default=1)
    def __str__(self):
        return '{} - {} - {} - {}'.format(self.lead.control_no, self.lead.status, self.calls_updated, self.no_of_followups)

class Folloup(models.Model):
    calldetails = models.ForeignKey(Calldetails, on_delete=models.CASCADE)
    remark = models.CharField(max_length=250)
    followups = models.IntegerField(default=0)

    calls_made = models.ForeignKey(Employee_details, on_delete=models.CASCADE, related_name='follo_calls_made', default=None)
    called_datetime = models.DateField(("Date"), default=datetime.date.today)
    called_meadium = models.CharField(max_length=10, default='phone')
    calls_updated = models.ForeignKey(Employee_details, on_delete=models.CASCADE, related_name='follo_calls_updated', default=None)

class Courses(models.Model):
    course = models.CharField(max_length=250)





