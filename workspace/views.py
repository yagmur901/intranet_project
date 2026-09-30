from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse, Http404
from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from pathlib import Path
from .models import WorkspaceFolder, WorkspaceFile
from .services import WorkspaceSyncService
import mimetypes
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.contrib.auth.decorators import login_required

def build_folder_tree(folder):
    """Her klasörün altına çocuklarını özyinelemeli (recursive) olarak bağlar."""
    return {
        'id': folder.id,
        'name': folder.name,
        'children': [build_folder_tree(child) for child in folder.children.all()],
        'files': [{'id': f.id, 'name': f.title, 'ext': f.file_extension} for f in folder.files.all()]
    }

@login_required
def workspace_list_view(request):
    if request.method == "POST" and "trigger_sync" in request.POST:
        stats = WorkspaceSyncService.sync()
        messages.success(
            request, 
            f"Senkronizasyon tamamlandı: {stats['created_files']} yeni dosya, {stats['deleted_files']} silinen dosya."
        )
        return redirect('workspace_list')

    folder_id = request.GET.get('folder', None)
    query = request.GET.get('q', '')

    # En üst seviye root klasörler
    root_folders = WorkspaceFolder.objects.filter(parent=None).prefetch_related('children')
    
    # Sınırsız derinlikteki klasör ağacı yapısı
    folder_tree = [build_folder_tree(f) for f in root_folders]

    active_folder = None
    if folder_id:
        active_folder = get_object_or_404(WorkspaceFolder, id=folder_id)
        files = WorkspaceFile.objects.filter(folder=active_folder)
    else:
        files = WorkspaceFile.objects.all()

    if query:
        clean_query = query.replace('I', 'ı').replace('İ', 'i').lower()
        files = files.filter(
            Q(title__unaccent__icontains=clean_query)
        )

    context = {
        'folder_tree': folder_tree,
        'active_folder': active_folder,
        'files': files,
        'query': query,
    }
    return render(request, 'workspace_list.html', context)


@login_required
@xframe_options_sameorigin
def workspace_download_view(request, file_id):
    file_obj = get_object_or_404(WorkspaceFile, id=file_id)
    full_path = Path(settings.SHARED_WORKSPACE_PATH) / file_obj.file_path

    if not full_path.exists() or not full_path.is_file():
        raise Http404("Dosya diskte bulunamadı.")

    is_preview = request.GET.get('preview') == '1'
    
    # Tarayıcının dosyayı nasıl açacağını belirlemesi için tipini tahmin et
    content_type, encoding = mimetypes.guess_type(str(full_path))
    
    # TXT, CSV, PY gibi düz metinler için tipi ve UTF-8'i zorla
    if file_obj.file_extension in ['txt', 'csv', 'py', 'json']:
        content_type = 'text/plain; charset=utf-8'

    # Dosyayı yanıta ekle
    response = FileResponse(open(full_path, 'rb'), content_type=content_type)
    
    # İndirme mi yoksa Önizleme mi olacağını ayarla
    if not is_preview:
        response['Content-Disposition'] = f'attachment; filename="{file_obj.title}"'
    else:
        response['Content-Disposition'] = f'inline; filename="{file_obj.title}"'
        
    return response

@login_required
def home_view(request):
    return render(request, 'home.html')