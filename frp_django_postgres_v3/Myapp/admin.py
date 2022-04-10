from django.contrib import admin

# Register your models here.
from Myapp.models.race_user import User
from Myapp.models.race_work import ClockList

admin.site.register(User)
admin.site.register(ClockList)