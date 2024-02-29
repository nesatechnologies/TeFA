from django.shortcuts import render, redirect
from .models import *

from datetime import datetime
from django.contrib import auth,messages

from .decorators import session_login_required

import csv


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
    print("%%%%%%%%%%%%%%%%%%%%111111111$$$$$$$$$$$$$$$$$$$$$$")
    if request.method == 'POST':
        print("%%%%%%%%%%%%%%%%%%%%22222222$$$$$$$$$$$$$$$$$$$$$$")
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
        print("%%%%%%%%%%%%%%%%%%%%$$$$$$$$$$$$$$$$$$$$$$")
        print(calls_made)
        print("%%%%%%%%%%%%%%%%%%%%$$$$$$$$$$$$$$$$$$$$$$")
        calls_updated_id = request.session.get('uid')
        calls_updated= Employee_details.objects.get(id=calls_updated_id)
        print(calls_updated)


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
    return render(request, 'folloup.html',{'data':data,'data1':data1})

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



