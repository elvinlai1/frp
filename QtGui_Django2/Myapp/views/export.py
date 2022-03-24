import codecs
import csv
from datetime import datetime, timedelta

from django.shortcuts import render
from rest_framework.decorators import api_view

from Myapp.models.race_work import ClockList
from django.forms import model_to_dict
from django.http.response import HttpResponse


def exportView(request):
    return render(request, 'export.html', locals())


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
    response.write(codecs.BOM_UTF8)
    response['Content-Disposition'] = f'attachment; filename={datetime.now()}.csv'
    response['Content-Type'] = 'application/octet-stream'
    writer = csv.writer(response)

    for data in data_list:
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
