from django.shortcuts import render
from Myapp.models.Employees import Employees
from Myapp.models.timestamps import Timestamps

from datetime import datetime

def index(request):

    # dashboard

    # Load last 10 recent activity TO DO
    #------------



    # Load all Timestamps find all in
    employees = Employees.objects.all()
    timestamps = Timestamps.objects.all()

    emp_activity=[]
    for e,ts in zip(employees,timestamps):

        emp_ts = datetime.fromtimestamp(float(ts.emp_timestamp))
        time = emp_ts.strftime("%H:%M:%S")

        emp_activity.append({
            'emp_num':e.emp_num,
            'emp_name':e.emp_name,
            'department':e.department,
            'time':time,
            'status': ts.emp_status
        })




    # Get emp_num and find department 

    

    #------------
    # Activity 
    # All Employee activity by most recent hour(?)  


    #Export Lists

    return render(request, 'test.html', locals())