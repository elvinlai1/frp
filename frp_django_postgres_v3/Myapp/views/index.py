from Myapp.models.employees import Employees
from Myapp.models.timestamps import Timestamps
from django.shortcuts import render

from datetime import datetime

def isBlank(params):
    if params is None:
        return True
    params = str(params).strip()
    if len(params) == 0:
        return True
    return False

def indexView(request):

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
     
        
    return render(request, 'index.html', locals())  

    '''

    def isBlank(params):
    if params is None:
        return True
    params = str(params).strip()
    if len(params) == 0:
        return True
    return False

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

    
    '''
   





