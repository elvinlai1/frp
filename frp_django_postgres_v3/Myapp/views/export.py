import codecs
import csv
from datetime import datetime, timedelta

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

from Myapp.models.employees import Employees
from Myapp.models.race_work import ClockList
from django.forms import model_to_dict
from django.http.response import HttpResponse
from Myapp.utils.timeUtils import time_format
from Myapp.models.timestamps import Timestamps


def exportView(request):
    return render(request, 'export.html', locals())


"""
new Api
"""


@api_view(["GET"])
def exportExcelTwo(request):
    typeValue = request.GET.get("type")
    day = request.GET.get("day")
    now_time = datetime.now()
    timestamps_list = Timestamps.objects.all()
    all_data = []
    for it in timestamps_list:
        emp = Employees.objects.get(employee_number=it.employee_number)
        d = model_to_dict(it, exclude=[])
        d.update(model_to_dict(emp, exclude=[]))
        all_data.append(d)
    # day

    if int(typeValue) == 1:
        action_time = now_time + timedelta(days=-int(day))
        print(action_time)
        response_json = list(
            filter(lambda x: action_time < datetime.fromtimestamp(float(x['timestamp'])) < now_time, all_data))
        if len(response_json) == 0:
            return Response(None)
        return exportCsv(response_json[0].keys(), response_json)
    # month
    else:
        q_day = datetime.strptime(day, '%Y-%m').day
        q_month = datetime.strptime(day, '%Y-%m').month

        def for_time(item):
            timestamp = datetime.fromtimestamp(float(item['timestamp']))
            i_day = timestamp.day
            i_month = timestamp.month
            print('{0},{1},{2},{3}'.format(q_day, q_month, i_day, i_month))
            return q_month.__eq__(i_month)

        response_json = list(filter(for_time, all_data))
        if len(response_json) == 0:
            return Response(None)
        return exportCsv(response_json[0].keys(), response_json)


"""
old Api
"""


@api_view(["GET"])
def exportExcel(request):
    typeValue = request.GET.get("type")
    day = request.GET.get("day")
    # day
    if int(typeValue) == 1:
        list_day = dateRange(int(day))
        data_list = ClockList.objects.filter(work_time__in=list_day)
        data = list(map(lambda x: model_to_dict(x, exclude=[]), data_list))
        return exportCsv(data[0].keys(), data)
    # month
    else:
        data_list = ClockList.objects.filter(work_time__icontains=day)
        # Use django.forms.model_to_dict turn data into dict, Note:ImageField cannot turn into dict
        data = list(map(lambda x: model_to_dict(x, exclude=[]), data_list))
        return exportCsv(data[0].keys(), data)


# export csv
def exportCsv(keys, data_list):
    response = HttpResponse(content_type='text/csv')
    # set Bom code
    response.charset = "utf-8-sig"
    response.write(codecs.BOM_UTF8)
    response['Content-Disposition'] = f'attachment; filename={datetime.now()}.csv'
    response['Content-Type'] = 'application/octet-stream'
    writer = csv.writer(response)
    writer.writerow(keys)
    for data in data_list:
        data['timestamp'] = datetime.fromtimestamp(float(data['timestamp']))
        writer.writerow(data.values())
    return response


# Get recent time
def dateRange(days):
    dates = []
    i = days
    begin = datetime.now().strftime("%Y-%m-%d")
    dt = datetime.strptime(begin, "%Y-%m-%d")
    date = begin[:]
    while i < days + 1:
        if i <= 0:
            break
        else:
            dates.append(date)
            dt = dt - timedelta(1)
            date = dt.strftime("%Y-%m-%d")
            i -= 1
    return dates
