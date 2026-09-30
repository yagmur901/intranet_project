from django.urls import path
from .views import document_list_view

urlpatterns = [
    path('', document_list_view, name='document_list'),
]