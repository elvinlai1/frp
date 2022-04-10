from django.urls import path, re_path
from .views import index, users
from .views import export
from .views import home

urlpatterns = [
    path('index', index.indexView),
    path('home', home.queryWorkList),
    path('queryList', home.queryWorkListByName),
    path('export', export.exportView),
    path('employee', users.indexView, name="users"),
    path('exportExcel', export.exportExcel),
    path('clock/edit/<int:id>', home.editClockItem, name="editClock"),
    path('clock/addView', home.addClockItem, name="addView"),
    path('clock/delete/<int:id>', home.delClockItem, name="delClock"),
    path('clock/edit', home.editHandler, name="delClockHandler"),
    path('clock/add', home.addHandler, name="addClockHandler"),
    path('employee/del', users.deleteEmployee, name="deleteEmployee"),
]
