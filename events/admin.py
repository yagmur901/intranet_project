from django.contrib import admin
from django import forms
from .models import Event

class EventAdminForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        widgets = {
            # tarayıcının varsayılan time picker'ını iptal edip standart metin inputu yap
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'vTextField'}),
        }

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    form = EventAdminForm
    list_display = ('title', 'start_date', 'location')