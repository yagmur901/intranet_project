from django.urls import path
from .views import workspace_list_view, workspace_download_view
from workspace import views

urlpatterns = [
    path('', workspace_list_view, name='workspace_list'),
    path('download/<int:file_id>/', workspace_download_view, name='workspace_download'),
    path('', views.home_view, name='home'),
]