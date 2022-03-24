from django.urls import path, re_path
from .views import index
from .views import export
from .views import home

urlpatterns = [
    path('index', index.indexView),
    path('home', home.queryWorkList),
    path('queryList', home.queryWorkListByName),
    path('export', export.exportView),
    path('exportExcel', export.exportExcel),
    path('clock/edit/<int:id>', home.editClockItem,name="editClock"),
    path('clock/delete/<int:id>', home.delClockItem,name="delClock"),
    path('clock/edit', home.editHandler,name="delClockHandler"),
]
