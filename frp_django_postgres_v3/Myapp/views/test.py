from multiprocessing import context
from django.shortcuts import render
from requests import request
from Myapp.models.timestamps import Timestamps
from Myapp.forms import newTimestamp
from datetime import datetime
from django.http import HttpResponseRedirect

def index(request):
    form = newTimestamp(request.POST)
    if request.method =="POST":
        action = request.POST["action"]
        if action=="timestamp":
            register_timestamp(request)
    else:     
        return render(request, 'test.html', {'form': form})

def get_Employee(request):    
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
    
     
def register_timestamp(request):
    form = newTimestamp(request.POST)
    if form.is_valid():
        form.save()
        return render(request, 'test.html', {'form':form})