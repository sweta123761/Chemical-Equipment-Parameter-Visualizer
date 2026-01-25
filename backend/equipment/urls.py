from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_csv, name='upload_csv'),
    path('history/', views.get_history, name='get_history'),
    path('report/', views.generate_report, name='generate_report'),
]
