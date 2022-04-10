from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

from Myapp.models.race_user import User


def isBlank(params):
    if params is None:
        return True
    params = str(params).strip()
    if len(params) == 0:
        return True
    return False


def indexView(request):
    user_list = list(User.objects.all().values('first_name', 'last_name', 'email', 'department', 'wage_per_hour', 'id'))
    return render(request, 'users.html', locals())


@api_view(['POST'])
def deleteEmployee(request):
    del_list = request.data.get('ids')
    try:
        User.objects.filter(id__in=del_list).delete()
        return Response({'message': 'delete success', 'code': 200})
    except Exception as e:
        return Response({'message': 'delete error', 'code': 500})
