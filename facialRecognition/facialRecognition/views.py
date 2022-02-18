from django.http import HttpResponse
from django.shortcuts import render

def homepage(request):
   # return HttpResponse("main")
   return render(request, 'homepage.html')

def login(request):
    return render(request, 'login.html')


def timesheet(request):
   return render(request, 'timesheets.html')

def profile(request):
  return render(request, 'profile.html')

def form(request):
    return render(request, 'form.html')
