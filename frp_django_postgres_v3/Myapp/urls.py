from django.urls import path, re_path
from .views import index, employees
from .views import export
from .views import activity
from .views import test
from .views import adminpanel

urlpatterns = [
    path('admin', adminpanel.index, name="admin"),
    path('', index.indexView, name="index"),
    path('activity', activity.queryWorkList, name="activity"),
    path('queryList', activity.queryWorkListByName),
    path('export', export.exportView, name="export"),
    path('employees', employees.indexView, name="employees"),
    path('exportExcel', export.exportExcel),
    path('clock/edit/<int:id>', activity.editClockItem, name="editClock"),
    path('clock/addView', activity.addClockItem, name="addView"),
    path('clock/delete/<int:id>', activity.delClockItem, name="delClock"),
    path('clock/edit', activity.editHandler, name="delClockHandler"),
    path('clock/add', activity.addHandler, name="addClockHandler"),
    path('employee/del', employees.deleteEmployee, name="deleteEmployee"),
    path('test', test.index, name="test"),
    path('search', test.getEmployee, name="search")
]
