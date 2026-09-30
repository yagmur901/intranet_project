from django.contrib import admin
from .models import WorkspaceFolder, WorkspaceFile

@admin.register(WorkspaceFolder)
class WorkspaceFolderAdmin(admin.ModelAdmin):
    list_display = ('name', 'relative_path', 'parent')
    search_fields = ('name', 'relative_path')

@admin.register(WorkspaceFile)
class WorkspaceFileAdmin(admin.ModelAdmin):
    list_display = ('title', 'folder', 'file_extension', 'file_size', 'last_modified')
    list_filter = ('folder', 'last_modified')
    search_fields = ('title', 'file_path')