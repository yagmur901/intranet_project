from django.contrib import admin
from .models import DocumentCategory, Document

@admin.register(DocumentCategory)
class DocumentCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'file_extension', 'file_size', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'description')

