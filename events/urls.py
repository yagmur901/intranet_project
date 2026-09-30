from django.urls import path
from .views import event_calendar_view, event_add_view, event_edit_view, event_delete_view

urlpatterns = [
    path('', event_calendar_view, name='event_calendar'),
    path('add/', event_add_view, name='event_add'),
    path('<int:event_id>/edit/', event_edit_view, name='event_edit'),
    path('<int:event_id>/delete/', event_delete_view, name='event_delete'),
]