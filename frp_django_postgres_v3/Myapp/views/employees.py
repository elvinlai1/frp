from datetime import datetime

from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

from Myapp.models.employees import Employees
from Myapp.models.race_user import User
from Myapp.models.timestamps import Timestamps


def isBlank(params):
    if params is None:
        return True
    params = str(params).strip()
    if len(params) == 0:
        return True
    return False


def indexView(request, numberId=None):
    tim_list = []
    if numberId:
        tim_list = Timestamps.objects.filter(employee_number=numberId)
    else:
        tim_list = Timestamps.objects.all()
    emp_list = Employees.objects.all()

    data = []

    for item in tim_list:
        current_user = emp_list.get(employee_number=item.employee_number)
        emp_ts = datetime.fromtimestamp(float(item.timestamp))
        time = emp_ts.strftime("%H:%M:%S")
        date = emp_ts.strftime("%m/%d/%y")
        c_item = {
            "date": date,
            "time": time,
            **model_to_dict(current_user),
            **model_to_dict(item),
        }
        print(c_item)
        data.append(c_item)
    return render(request, 'employees.html', locals())


def editView(request, id):
    timestamps = Timestamps.objects.get(id=id)
    emp_ts = datetime.fromtimestamp(float(timestamps.timestamp))
    time = emp_ts.strftime("%H:%M:%S")
    date = emp_ts.strftime("%Y-%d-%m")
    clock_item = {
        'time': time,
        'date': date,
        'status': timestamps.status
    }
    print(clock_item)
    return render(request, 'editTimestamps.html', locals())


@api_view(['POST'])
def editViewItem(request):
    data = request.data
    old_record = Timestamps.objects.get(id=data.get("id"))
    try:
        current_times = datetime.strptime(data.get('timer'), '%Y-%d-%m %H:%M:%S')
        old_record.status = data.get('status')
        old_record.timestamp = current_times.timestamp()
        old_record.save()
        return Response({'message': 'edit success', 'code': 200})
    except Exception as e:
        return Response({'message': 'edit error', 'code': 500})


@api_view(['POST'])
def deleteEmployee(request):
    id = request.data.get('id')
    print(id)
    try:
        Timestamps.objects.filter(id=id).delete()
        return Response({'message': 'delete success', 'code': 200})
    except Exception as e:
        return Response({'message': 'delete error', 'code': 500})
