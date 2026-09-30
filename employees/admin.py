from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('edit_button', 'first_name', 'last_name', 'short_name', 'department', 'email', 'phone_number')
    list_display_links = ('edit_button',)
    list_editable = ('first_name', 'last_name', 'short_name', 'department', 'email', 'phone_number')
    search_fields = ('first_name', 'last_name', 'short_name', 'department', 'email', 'phone_number')
    list_filter = ('department',)
    ordering = ('-id',)
    list_per_page = 50

    @admin.display(description="")
    def edit_button(self, obj):
        url = reverse('admin:employees_employee_change', args=[obj.id])
        return format_html(
            '<a href="{}" title="Düzenle" style="color: #4b5563; font-size: 14px; text-decoration: none; padding: 2px 7px; border-radius: 4px; border: 1px solid #d1d5db; background-color: #f9fafb; display: inline-block;">✎</a>',
            url
        )