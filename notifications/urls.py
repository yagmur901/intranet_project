from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.notification_list, name='list'),
    path('read-all/', views.mark_all_as_read, name='mark_all_as_read'),
    path('read/<int:notif_id>/', views.read_and_redirect, name='read_and_redirect'),
]