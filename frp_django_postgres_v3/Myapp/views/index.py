from django.db.models import Count
from django.shortcuts import render
from Myapp.models.race_user import User
from Myapp.models.race_work import ClockList
from Myapp.models.employees import Employees
from Myapp.utils.timeUtils import time_format
from Myapp.forms import NewUserForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib import messages
from Myapp.forms import newTimestamp

# request.user.is_authenticated()
def isBlank(params):
    if params is None:
        return True
    params = str(params).strip()
    if len(params) == 0:
        return True
    return False


def indexView(request):
    current_date = time_format(format='%Y-%m-%d')
    # get all the data from 'work' table
    clock_list = ClockList.objects.filter(work_time__contains=current_date)
    work_list = []
    for wk in clock_list:
        work_list.append({
            'id': wk.id,
            'employee': wk.employee,
            'work_time': wk.work_time,
            'status': True if not (isBlank(wk.in_time)) and not (isBlank(wk.out_time)) else False
        })
    # count user in each department
    department_user = User.objects.values('department').annotate(count=Count('first_name')).values('department',
                                                                                                   'count')
    # get departments detail
    for prt in department_user:
        count = ClockList.objects.filter(work_time__contains=current_date,
                                         department__iexact=prt['department']).distinct().count()
        prt['work'] = count
        prt['not_work'] = prt['count'] - count
    return render(request, 'index.html', locals())


def register_request(request):
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

     


