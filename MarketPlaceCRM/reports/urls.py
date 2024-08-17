from django.urls import path
from .views import generate_report, view_reports, save_report, view_report, download_report, delete_report


app_name = 'reports'


urlpatterns = [
    path('generate_report/', generate_report, name='generate_report'),
    path('view_reports/', view_reports, name='view_reports'),
    path('save_report/', save_report, name='save_report'),
    path('download/<int:report_id>/', download_report , name='download_report'),
    path('view_report/<int:report_id>/', view_report, name='view_report'),
    path('delete/<int:report_id>/', delete_report, name='delete_report'),
]
