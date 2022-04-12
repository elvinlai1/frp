from sqlite3 import Time
from django.contrib import admin

# Register your models here.
from Myapp.models.race_user import User
from Myapp.models.race_work import ClockList

from Myapp.models.face import Face
from Myapp.models.Employees import Employees
from Myapp.models.timestamps import Timestamps

admin.site.register(User)
admin.site.register(ClockList)

admin.site.register(Face)
admin.site.register(Employees)
admin.site.register(Timestamps)