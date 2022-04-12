from django.db.models import Count
from django.shortcuts import render
from Myapp.models.race_user import User
from Myapp.models.race_work import ClockList
from Myapp.utils.timeUtils import time_format
from Myapp.forms import NewUserForm
from django.contrib.auth.models import User, auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

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
    if request.method=='POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.info(request, f'Created user {username}') 
            return render(request, 'register.html', {'form':form})
    else:
        form = NewUserForm()
    return render(request, 'register.html', {'form':form})
