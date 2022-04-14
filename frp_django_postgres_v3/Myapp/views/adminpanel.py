from django.shortcuts import render
from django.http.response import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import messages
from Myapp.forms import newTimestamp
from Myapp.forms import NewUserForm
from Myapp.models.employees import Employees

def index(request):
    reg_emp = NewUserForm(request.POST)
    if request.method=='POST':
        action = request.POST["action"]
        if action=="submit":
            register_employee(request)
        if action=="delete":
            delete_employee(request)
        if action=="timestamp":
            register_timestamp(request)
        
    reg_emp = NewUserForm()
    reg_ts = newTimestamp()
    context = {
        'reg':reg_emp,
        'reg_ts':reg_ts
    }
    return render(request, 'register.html', context)

def delete_employee(request):
    x = request.POST['employee_delete']
    try:
        record = Employees.objects.get(employee_number = x)
        record.delete()
        messages.success(request, f'Employee Number {x} Deleted')
        return HttpResponseRedirect('')
       
    except:
        messages.error(request, f'Employee Number {x} does not exist')

def register_employee(request):
    form = NewUserForm(request.POST)
    if form.is_valid():
        form.save()
        employee_number = form.cleaned_data.get('employee_number')
        messages.info(request, f'Employee number: {employee_number} created') 
        return HttpResponseRedirect('')
    else: 
        employee_number = request.POST.get('employee_number')
        messages.error(request, f'Employee number: {employee_number} already exists')

def register_timestamp(request):
    form2 = newTimestamp(request.POST)
    if form2.is_valid():
        form2.save()

     