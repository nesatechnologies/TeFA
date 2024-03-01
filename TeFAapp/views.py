from django.shortcuts import render, redirect
from .models import *

from datetime import datetime
from django.contrib import auth,messages

from .decorators import session_login_required

import csv
from django.db.models import Q
import openpyxl
from openpyxl import Workbook
from django.http import HttpResponse

from django.template.loader import render_to_string

# Create your views here.
@session_login_required
def home(request):
    data = Lead.objects.filter(status=0)
    no_contact = Lead.objects.all().count()
    wait_call = Lead.objects.filter(status=0).count()
    conformed = Lead.objects.filter(status=1).count()
    need_following = Lead.objects.filter(status=2).count()
    denied = Lead.objects.filter(status=3).count()
    return render(request, 'home.html',{'data':data, 'wait_call':wait_call, 'no_contact':no_contact,
                                        'conformed':conformed, 'need_following':need_following, 'denied':denied})
def conformed(request):
    data = Calldetails.objects.filter(lead__status=1)
    return render(request, 'conformed.html', {'data':data})
def need_following(request):
    data = Calldetails.objects.filter(lead__status=2)
    return render(request, 'need_following.html', {'data':data})
def denied(request):
    data = Calldetails.objects.filter(lead__status=3)
    return render(request, 'denied.html', {'data':data})
def add_customer(request):
    # inputing user data from employee side form
    if request.method == 'POST':
        phone_no = request.POST.get('phone_no')
        name = request.POST.get('name')
        course = request.POST.get('course')
        email = request.POST.get('email')
        place = request.POST.get('place')
        lead_date = request.POST.get('lead_date')
        remark = request.POST.get('remark')
        source = request.POST.get('source')
        degree = request.POST.get('degree')

        ######  control_no part operations ######
        # Get the last row based on the primary key
        last_row = Lead.objects.last()
        if last_row:
            # Access attributes of the last row
            print("Last row:", last_row.control_no)
            control_no = last_row.control_no
            control_no += 1
        else:
            print("Table is empty")
            control_no = 5000


        ######### starting lead_no part ###########
        ## using entered 'lead_date' can used to create special type of code for "lead_no".
        ## month-year-Lnumber eg : feb-24-L1


        ### month first three letter taking part
        print(f"$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$lead_date = {lead_date}")
        # Parse the date string
        date_string = lead_date
        date_object = datetime.strptime(date_string, "%Y-%m-%d")
        # Get the English month name first three letters using %b
        english_month = date_object.strftime("%b")
        # print("English month:", english_month)

        #### year last two digit taking part
        # Parse the date string
        date_string = lead_date
        date_object = datetime.strptime(date_string, "%Y-%m-%d")
        # Get the last two digits of the year
        last_two_digits_year = date_object.strftime("%y")
        print("Last two digits of the year:", last_two_digits_year)

        ### retrieve last updated row from data base and compire to done operation
        if last_row:
            # Access "lead date" attributes of the last row.
            lead_given_date1 =last_row.lead_given_date
            print("past lead_given_date:", lead_given_date1)

            # Parse the date strings into datetime objects
            print(type(lead_given_date1))
            print(type(lead_date))
            lead_given_date1_parse = datetime.strptime(str(lead_given_date1), "%Y-%m-%d")
            lead_date_parse = datetime.strptime(lead_date, "%Y-%m-%d")
            print(lead_given_date1_parse)
            print(lead_date_parse)

            ## comparing the previous row lead_date and new entered one lead_date
            if lead_given_date1_parse == lead_date_parse:
                print("same")
                # in the case of same date old one same lead_no is giving
                lead_no = last_row.lead_no
            else:

                try:
                    ### check data before entered if lend date already entered take same lead_no( not only checking just previous row )
                    print("different")
                    lended_date_details = Lead.objects.get(lead_given_date = lead_date)
                    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                    print(lended_date_details.lead_no)
                    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                    lead_no = lended_date_details.lead_no

                except:
                    print("different")
                    # split to a list to compire its month and year
                    x = str(lead_given_date1_parse).split("-")
                    y = str(lead_date_parse).split("-")
                    print(x)
                    print(y)
                    # in the case of different year or month compired to previous one just set val =1
                    if x[0] != y[0] or x[1] != y[1]:
                        val = 1
                        lead_no = english_month + '-' + last_two_digits_year + '-' + 'L' + str(val)
                    else:
                        # in the case of previous and new lend date month & year same
                        bfore_lead_no= last_row.lead_no
                        print(type(bfore_lead_no))
                        # taking number from previous lend no from last position and add 1 to it
                        print(bfore_lead_no[-1])
                        a = bfore_lead_no[-1]
                        val = int(a) + 1
                        lead_no = english_month + '-' + last_two_digits_year + '-' + 'L' + str(val)
        else:
            val = 1
            lead_no = english_month + '-' + last_two_digits_year + '-' + 'L' + str(val)

        # lead_no =english_month+'-'+last_two_digits_year+'-'+'L'+str(val)

        data = Lead(lead_given_date=lead_date, name=name, course=course, phone_no=phone_no, email=email, place=place, remark=remark, control_no=control_no, lead_no=lead_no, source=source, degree=degree)
        data.save()
        return redirect('home')
    return render(request, 'add_customer.html')

def delete(request, id):
    if request.method == 'POST':
        data = Lead.objects.get(id=id)
        data.delete()
        return redirect('home')
    data = Lead.objects.filter(id=id)
    return render(request, 'delete.html',{'data':data})

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if username != '' and password != '':
            if Employee_details.objects.filter(user_name=username, password=password).exists():
                data = Employee_details.objects.filter(user_name=username, password=password).values('name', 'emp_id', 'id').first()
                print(data)
                request.session['name'] = data['name']
                request.session['emp_id'] = data['emp_id']
                request.session['username'] = username
                request.session['password'] = password
                request.session['uid'] = data['id']
                return redirect('home')
            else:
                return render(request, 'register_user.html', {'msg': "invalid"})
        else:
            messages.info(request, "enter all inputs")
            return redirect('login')
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        name = request.POST['name']
        empid = request.POST['empid']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        if username != '' and password != '' and cpassword !='' and empid !='' and name !='':
            if password == cpassword:
                if Employee_details.objects.filter(user_name=username).exists():
                    messages.info(request, "username is Already taken")
                elif Employee_details.objects.filter(emp_id=empid).exists():
                    messages.info(request, "Employee id is Already taken")
                else:
                    user = Employee_details(user_name=username,password=password,name=name,emp_id=empid)
                    user.save()
                    messages.info(request, "user created")
            else:
                messages.info(request, "passwords not matched")
                return redirect('register')
        else:
            messages.info(request, "enter all inputs")
            return redirect('register')
    return render(request, 'register.html')

def logout(request):
    del request.session['name']
    del request.session['emp_id']
    del request.session['username']
    del request.session['password']
    del request.session['uid']
    return redirect('login')

def call(request,id):
    if request.method == 'POST':
        selected_value = request.POST['name']
        if selected_value:
            name, emp_id = selected_value.split('|')
            # Now you have name and emp_id separately
            # Do whatever you want with these values
        else:
            # Handle case when no option is selected
            pass
        status = request.POST['status']
        called_meadium = request.POST['called_meadium']
        emp_remark = request.POST['remark']
        lead = Lead.objects.get(id=id)
        calls_made= Employee_details.objects.get(emp_id=emp_id)
        calls_updated_id = request.session.get('uid')
        calls_updated= Employee_details.objects.get(id=calls_updated_id)

        userdata = Calldetails(lead=lead, calls_made=calls_made, emp_remark=emp_remark, called_meadium=called_meadium, calls_updated=calls_updated)
        userdata.save()
        lead.status = status
        lead.save()
        # Redirect to the home page with refresh parameter
        return redirect('/')
    data = Lead.objects.filter(id=id)
    data1 = Employee_details.objects.all()
    return render(request, 'call.html',{'data':data,'data1':data1})

def followup(request, id):
    if request.method == 'POST':
        selected_value = request.POST['name']
        if selected_value:
            name, emp_id = selected_value.split('|')
            # Now you have name and emp_id separately
            # Do whatever you want with these values
        else:
            # Handle case when no option is selected
            pass
        status = request.POST['status']

        called_meadium = request.POST['called_meadium']
        remark = request.POST['remark']

        calldetails = Calldetails.objects.get(id=id)
        calls_made= Employee_details.objects.get(emp_id=emp_id)
        calls_updated_id = request.session.get('uid')
        calls_updated= Employee_details.objects.get(id=calls_updated_id)


        userdata = Folloup(calldetails=calldetails, remark=remark, called_meadium=called_meadium, calls_made=calls_made, calls_updated=calls_updated)
        userdata.save()

        current_followups = calldetails.no_of_followups
        calldetails.no_of_followups = current_followups + 1
        calldetails.save()

        calldetails.lead.status = status
        calldetails.lead.save()
        return redirect('/')
    data = Calldetails.objects.filter(id=id)
    data1 = Employee_details.objects.all()
    data2 = Folloup.objects.filter(calldetails__id=id)
    data3 = Calldetails.objects.get(id=id)
    return render(request, 'folloup.html',{'data':data,'data1':data1,'data2':data2,'data3':data3})

def followup_actions(request,id):
    data = Folloup.objects.filter(calldetails__id = id)
    data1 = Calldetails.objects.get(id=id)
    return render(request,'followup_actions.html',{'data':data,'data1':data1})

def upload_csv(request):
    message = ""  # Default message
    csv_data = None  # Default CSV data
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        if csv_file.name.endswith('.csv'):
            # Process the uploaded CSV file
            try:
                # Decode and process the CSV file
                decoded_file = csv_file.read().decode('utf-8')
                csv_data = csv.reader(decoded_file.splitlines())
                for row in csv_data:
                    # Process each row of the CSV file
                    if row[0] == 'SL.NO':
                        continue
                    else:
                        print(row)
                        control_no = int(row[1])
                        lead_no = str(row[2])

                        # Input date string
                        date_string = str(row[3])
                        # Parse the date string into a datetime object
                        date_object = datetime.strptime(date_string, "%d/%m/%Y")
                        # Format the datetime object in the desired format
                        formatted_date = date_object.strftime("%Y-%m-%d")
                        lead_given_date = formatted_date

                        source = str(row[4])
                        name = str(row[5])
                        phone_no = int(row[6])
                        email = (row[7])
                        place = str(row[8])
                        degree = str(row[9])
                        course = str(row[10])
                        remark = str(row[11])

                        data = Lead(lead_given_date=lead_given_date, name=name, course=course, phone_no=phone_no, email=email,
                                    place=place, remark=remark, control_no=control_no, lead_no=lead_no, source=source,
                                    degree=degree)
                        data.save()



                message = "CSV file uploaded and processed successfully."
            except Exception as e:
                message = f"Error processing CSV file: {e}"
        else:
            message = "Please upload a valid CSV file."
    else:
        message = "No file uploaded."
    return redirect('/')

def contactbook(request):
    data = Lead.objects.all()
    return render(request,'contactbook.html',{'data':data})

def searchresult(request):
    products= None
    query= None
    if 'q' in request.GET:
        query = request.GET.get('q')
        products= Lead.objects.all().filter(Q(control_no__contains = query) | Q(date_time_added__contains = query) | Q(lead_given_date__contains = query) | Q(lead_no__contains = query) | Q(name__contains = query) | Q(course__contains = query) | Q(phone_no__contains = query) | Q(email__contains = query) | Q(place__contains = query) | Q(remark__contains = query) | Q(status__contains = query) | Q(source__contains = query) | Q(degree__contains = query))
        return render(request, 'search.html', {'query':query, 'products':products})

def export_to_excel(request):
    # Create a new workbook
    wb = Workbook()

    # Activate the first sheet
    ws = wb.active
    ws.title = "Contactbook Data"

    # Write headers
    headers = ["Control No", "Date Time Added", "Lead Given Date", "Lead No", "Name", "Course", "Phone No", "Email", "Place", "Remark", "Status", "Source", "Degree"]
    ws.append(headers)

    # Fetch data from Lead model
    leads = Lead.objects.all()

    # Write data rows
    for lead in leads:
        statusval = ""
        if lead.status == 0:
            statusval = "wait for call"
        elif lead.status == 1:
            statusval = "conformed"
        elif lead.status == 2:
            statusval = "need following"
        elif lead.status == 3:
            statusval = "denied"

        row = [lead.control_no, lead.date_time_added, lead.lead_given_date, lead.lead_no, lead.name, lead.course, lead.phone_no, lead.email, lead.place, lead.remark, statusval, lead.source, lead.degree]
        ws.append(row)

    # Create a response object
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=contactbook.xlsx'

    # Save the workbook to the response
    wb.save(response)

    return response

def need_following_export_to_excel(request):

    # data_need_following = Calldetails.objects.filter(lead__status=2)
    #
    # # Initialize empty lists to store IDs
    # calldetails_ids = []
    #
    # # Extract row IDs from data_need_following
    # for calldetail in data_need_following:
    #     calldetails_ids.append(calldetail.id)
    #
    # print(calldetails_ids)
    #
    # # Create a new workbook
    # wb = Workbook()
    #
    # # Activate the first sheet
    # ws = wb.active
    # ws.title = "Need following Data"
    #
    # headers = ["Control No", "Date Time Added", "Lead Given Date", "Lead No", "Name", "Course", "Phone No", "Email",
    #            "Place", "Remark", "Source", "Degree", "", "", "initial call"]
    # row1 = ["", "", "", "", "", "", "", "", "", "", "", "", "", "",
    #        "calls_made", "calls_updated", "called_datetime", "called_meadium", "emp_remark"]
    # # Write headers
    # ws.append(headers)
    # ws.append(row1)
    # for ids in calldetails_ids:
    #     data = Folloup.objects.filter(calldetails__id=ids)
    #     data1 = Calldetails.objects.get(id=ids)
    #
    #     row = [data1.lead.control_no, data1.lead.date_time_added, data1.lead.lead_given_date, data1.lead.lead_no, data1.lead.name, data1.lead.course, data1.lead.phone_no, data1.lead.email, data1.lead.place, data1.lead.remark, data1.lead.source, data1.lead.degree,"","", data1.calls_made.name, data1.calls_updated.name, data1.called_datetime, data1.called_meadium, data1.emp_remark]
    #     ws.append(row)
    #
    # # Create a response object
    # response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    # response['Content-Disposition'] = 'attachment; filename=needfollowing.xlsx'
    #
    # # Save the workbook to the response
    # wb.save(response)
    #
    # return response
    calldetails_data = Calldetails.objects.filter(lead__status=2)

    # Create a new workbook
    wb = Workbook()

    # Activate the first sheet
    ws = wb.active
    ws.title = "Need following Data"

    def get_folloup_headers(calldetail):
        """
        Generates follow-up headers based on the number of follow-up entries for a calldetail.
        """
        folloup_count = calldetail.folloup_set.all().count()
        return ["Folloup Remark", "Folloup Updated", "Made By"] * folloup_count

    # Define base headers
    base_headers = [
        "Control No",
        "Date Time Added",
        "Lead Given Date",
        "Lead No",
        "Name",
        "Course",
        "Phone No",
        "Email",
        "Place",
        "Remark",
        "Source",
        "Degree",
        "Calls Made",
        "Calls Updated",
        "Called Datetime",
        "Called Medium",
        "Employee Remark",
    ]

    # Combine base headers and dynamically generated follow-up headers
    headers = base_headers + sum([get_folloup_headers(calldetail) for calldetail in calldetails_data], [])

    # Write headers to the first row only
    ws.append(headers)

    for calldetail in calldetails_data:
        # Initialize empty lists to store folloup details
        folloup_remarks = []
        folloup_updated = []
        call_made_by = []

        # Retrieve related Folloup data
        folloup_data = Folloup.objects.filter(calldetails=calldetail)

        # Extract folloup details into separate lists
        for folloup in folloup_data:
            folloup_remarks.append(folloup.remark)
            folloup_updated.append(folloup.called_datetime.strftime("%Y-%m-%d %H:%M:%S"))  # Format date/time
            call_made_by.append(folloup.calls_made.name)  # Assuming 'name' is the relevant field

        # Extract Calldetails data
        row = []  # Create an empty row

        # Add lead details
        row.extend([
            calldetail.lead.control_no,
            calldetail.lead.date_time_added,
            calldetail.lead.lead_given_date,
            calldetail.lead.lead_no,
            calldetail.lead.name,
            calldetail.lead.course,
            calldetail.lead.phone_no,
            calldetail.lead.email,
            calldetail.lead.place,
            calldetail.lead.remark,
            calldetail.lead.source,
            calldetail.lead.degree,
            calldetail.calls_made.name,  # Assuming 'name' is the relevant field
            calldetail.calls_updated.name,  # Assuming 'name' is the relevant field
            calldetail.called_datetime,
            calldetail.called_meadium,
            calldetail.emp_remark,
        ])

        # Add folloup details with corresponding headings
        for remark, updated, made_by in zip(folloup_remarks, folloup_updated, call_made_by):
            row.append(remark)
            row.append(updated)
            row.append(made_by)

        # Write the combined row to the worksheet
        ws.append(row)

    # Create a response object
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=needfollowing.xlsx'

    # Save the workbook to the response
    wb.save(response)
    return response