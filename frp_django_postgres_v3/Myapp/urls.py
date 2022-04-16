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

    path('employees/<str:numberId>', employees.indexView, name="employees"),
    path('employees', employees.indexView, name="employees"),

    path('employeesEdit/<int:id>', employees.editView, name="editEmployees"),
    path('employeesEdit/edit', employees.editViewItem, name="editEmployeesItem"),
    path('employeesEdit/delete', employees.deleteEmployee, name="deleteEmployees"),



    path('exportExcel', export.exportExcelTwo),
    path('clock/edit/<int:id>', activity.editClockItem, name="editClock"),
    path('clock/addView', activity.addClockItem, name="addView"),
    path('clock/delete/<int:id>', activity.delClockItem, name="delClock"),
    path('clock/edit', activity.editHandler, name="delClockHandler"),
    path('clock/add', activity.addHandler, name="addClockHandler"),
    path('employee/del', employees.deleteEmployee, name="deleteEmployee"),
    path('queryActivity', activity.queryActivity, name="queryActivity"),
]
