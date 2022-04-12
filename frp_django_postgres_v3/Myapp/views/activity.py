import json
from datetime import datetime
from urllib.parse import unquote

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from Myapp.models.race_user import User
from Myapp.models.race_work import ClockList
from Myapp.utils.timeUtils import secondsToHours
from Myapp.views.index import isBlank
from Myapp.utils.myEncoder import MyEncoder


# list
def queryWorkList(request):
    user_list = User.objects.all().values('id', 'first_name');
    return render(request, 'activity.html', locals())


def addClockItem(request):
    user_list = User.objects.all().values('id', 'first_name');
    return render(request, 'addClock.html', locals())


# edit
def editClockItem(request, id):
    clock_item = ClockList.objects.get(id=id)
    print(datetime.strptime(clock_item.in_time, '%H:%M:%S'))
    return render(request, 'editClock.html', locals())


@api_view(["POST"])
def delClockItem(request, id):
    try:
        record = ClockList.objects.get(id=int(id))
        record.delete()
        print("Record deleted successfully!")
        return Response({'message': 'delete success', 'code': 200})
    except:
        print("Record doesn't exists")
        return Response({'message': 'delete error', 'code': 500})


@api_view(["POST"])
def editHandler(request):
    data = request.data
    old_record = ClockList.objects.get(id=data.get("id"))
    try:
        old_record.in_time = data.get('in_time') + old_record.in_time[5:]
        old_record.out_time = data.get('out_time') + old_record.out_time[5:]
        old_record.work_time = data.get('work_time')
        old_record.notes = data.get('notes')
        old_record.deduction = data.get('deduction') if int(data.get('deduction')) > 0 else 0
        # computed time
        in_time = datetime.strptime(data.get('in_time'), '%H:%M')
        out_time = datetime.strptime(data.get('out_time'), '%H:%M')
        timestamp = (out_time - in_time).seconds
        days, hours, minutes, second = secondsToHours(timestamp * 1000)
        old_record.hours = f'{"0" + str(hours) if hours < 10 else hours}:{"0" + str(minutes) if minutes < 10 else minutes} '

        old_record.save()
        return Response({'message': 'edit success', 'code': 200})
    except Exception as e:
        print(e)
        return Response({'message': 'edit error', 'code': 500})


@api_view(["POST"])
def addHandler(request):
    data = request.data
    employee = data.get('employee')
    try:
        current_second = datetime.now().second
        second = str(current_second) if current_second >= 10 else '0' + str(current_second)
        second = second.strip()
        print("second===>" + second)
        record = ClockList(
            employee=employee,
            department=User.objects.get(first_name=employee).department,
            in_time=data.get('in_time') + ':' + str(second),
            out_time=data.get('out_time') + ':' + str(second)
        )
        print(record.in_time)
        print(record.out_time)
        record.work_time = data.get('work_time')
        record.notes = data.get('notes')
        record.deduction = data.get('deduction') if int(data.get('deduction')) > 0 else 0
        # computed time
        in_time = datetime.strptime(record.in_time, '%H:%M:%S')
        out_time = datetime.strptime(record.out_time, '%H:%M:%S')
        timestamp = (out_time - in_time).seconds
        days, hours, minutes, second = secondsToHours(timestamp * 1000)
        record.hours = f'{"0" + str(hours) if hours < 10 else hours}:{"0" + str(minutes) if minutes < 10 else minutes} '
        record.save()
        return Response({'message': 'add success', 'code': 200})
    except Exception as e:
        print(e)
        return Response({'message': 'add error', 'code': 500})


@api_view(['GET'])
def queryWorkListByName(request):
    first_name = request.GET['first_name']
    clock_list = []
    if isBlank(first_name):
        clock_list = ClockList.objects.all()
    else:
        clock_list = ClockList.objects.filter(employee=first_name)

    response_json = json.dumps(clock_list.values(), cls=MyEncoder)
    return Response(json.loads(response_json))


def transform(str_param):
    param = {i[0]: unquote(i[1]).encode('utf-8').decode('utf-8') for i in [i.split('=') for i in str_param.split('&')]}
    return param
