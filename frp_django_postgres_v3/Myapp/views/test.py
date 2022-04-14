from multiprocessing import context
from tracemalloc import take_snapshot
from django.shortcuts import render
from requests import request
from Myapp.models.employees import Employees
from Myapp.models.timestamps import Timestamps
from Myapp.forms import newTimestamp
from django.contrib import messages
from datetime import datetime
from django.http import HttpResponseRedirect

def index(request):
    # dashboard

    # Load last 10 recent activity TO DO
    #------------


    # Recent Activity Log
    # Get all timestamp 
    # For each timestamp 
    # Get info by employee number
    #
    timestamps = Timestamps.objects.all()


    emp_activity=[]
    for ts in timestamps:
        
        employee = Employees.objects.filter(employee_number=ts.employee_number)
        #print(employee[0].employee_number)
        
        emp_ts = datetime.fromtimestamp(float(ts.timestamp))
        time = emp_ts.strftime("%H:%M:%S")
        date = emp_ts.strftime("%m/%d/%y")

        emp_activity.append({
            'name':employee[0].employee_name,
            'number':ts.employee_number,
            'department':employee[0].department,
            'date': date,
            'time':time,
            'status': ts.status
        })
     
        

    return render(request, 'test.html', locals())

def getEmployee(request):
    if request.method =="POST":
        searched = request.POST["searched"]
        emp = Timestamps.objects.filter(employee_number=searched)
        emp2 = []
        for e in emp: 

            emp_ts = datetime.fromtimestamp(float(e.timestamp))
            time = emp_ts.strftime("%H:%M:%S") 
            date = emp_ts.strftime("%m/%d/%y")   

            emp2.append({
                'number':e.employee_number,
                'date':date,
                'time':time,
                'status':e.status
            })

        return render(request, 'test.html', {'searched':searched, 'emp2':emp2})
    else: 
        return render(request, 'test.html', locals())

    
    '''timestamp = Timestamps()
    query = request.GET.get("employee_number")
    
    emp = timestamp.objects.filter(employee_number=query)

    emp2 = []
    for e in emp: 

        emp_ts = datetime.fromtimestamp(float(e.timestamp))
        time = emp_ts.strftime("%H:%M:%S") 
        date = emp_ts.strftime("%m/%d/%y")   

        emp2.append({
            'number':e.employee_number,
            'date':date,
            'time':time,
            'status':e.status
        })
    print(emp2)
    '''
