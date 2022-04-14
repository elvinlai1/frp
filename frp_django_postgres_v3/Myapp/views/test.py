from django.shortcuts import render
from Myapp.models.employees import Employees
from Myapp.models.timestamps import Timestamps
from django.contrib import messages

from datetime import datetime

def index(request):

    # dashboard

    # Load last 10 recent activity TO DO
    #------------



    # Recent Activity Log
    employees = Employees.objects.all()
    timestamps = Timestamps.objects.all()

    emp_activity=[]
    for e,ts in zip(employees,timestamps):

        emp_ts = datetime.fromtimestamp(float(ts.timestamp))
        time = emp_ts.strftime("%H:%M:%S")
        date = emp_ts.strftime("%m/%d/%y")

        emp_activity.append({
            'name':e.employee_number,
            'number':e.employee_name,
            'department':e.department,
            'date': date,
            'time':time,
            'status': ts.status
        })

    emp = Timestamps.objects.filter(employee_number=100)

    emp2 = []
    for e in emp: 

        emp_ts2 = datetime.fromtimestamp(float(e.timestamp))
        time = emp_ts2.strftime("%H:%M:%S") 
        date = emp_ts.strftime("%m/%d/%y")   

        emp2.append({
            'number':e.employee_number,
            'date':date,
            'time':time,
            'status':e.status
        })



    #Export Lists

    return render(request, 'test.html', locals())