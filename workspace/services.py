from pathlib import Path
from datetime import datetime
from django.conf import settings
from django.utils import timezone
from .models import WorkspaceFolder, WorkspaceFile

class WorkspaceSyncService:
    @staticmethod
    def sync():
        base_path = Path(settings.SHARED_WORKSPACE_PATH)
        
        if not base_path.exists():
            base_path.mkdir(parents=True, exist_ok=True)
            return {"created_folders": 0, "created_files": 0, "deleted_files": 0}

        created_folders = 0
        created_files = 0
        
        # Klasör hiyerarşisi
        all_dirs = [p for p in base_path.rglob('*') if p.is_dir()]
        all_dirs.sort(key=lambda p: len(p.parts))

        root_folder_obj, _ = WorkspaceFolder.objects.get_or_create(
            relative_path="",
            defaults={"name": base_path.name, "parent": None}
        )

        folder_mapping = {"": root_folder_obj}

        for d in all_dirs:
            rel = str(d.relative_to(base_path)).replace('\\', '/')
            parent_rel = str(d.parent.relative_to(base_path)).replace('\\', '/') if d.parent != base_path else ""
            
            parent_obj = folder_mapping.get(parent_rel, root_folder_obj)
            
            folder_obj, created = WorkspaceFolder.objects.get_or_create(
                relative_path=rel,
                defaults={"name": d.name, "parent": parent_obj}
            )
            if created:
                created_folders += 1
            folder_mapping[rel] = folder_obj

        # Dosyaları tara ve eşitle
        seen_file_paths = set()
        all_files = [p for p in base_path.rglob('*') if p.is_file()]

        for f in all_files:
            rel_folder_path = str(f.parent.relative_to(base_path)).replace('\\', '/') if f.parent != base_path else ""
            folder_obj = folder_mapping.get(rel_folder_path, root_folder_obj)

            rel_file_path = str(f.relative_to(base_path)).replace('\\', '/')
            seen_file_paths.add(rel_file_path)

            stat = f.stat()
            file_mtime = timezone.make_aware(datetime.fromtimestamp(stat.st_mtime))

            file_obj, created = WorkspaceFile.objects.update_or_create(
                file_path=rel_file_path,
                defaults={
                    "title": f.name,
                    "folder": folder_obj,
                    "file_size_bytes": stat.st_size,
                    "last_modified": file_mtime,
                }
            )
            if created:
                created_files += 1

        # Silinen dosyaları ve boş kalan klasörleri temizle
        deleted_files, _ = WorkspaceFile.objects.exclude(file_path__in=seen_file_paths).delete()
        valid_rel_dirs = {""} | {str(d.relative_to(base_path)).replace('\\', '/') for d in all_dirs}
        WorkspaceFolder.objects.exclude(relative_path__in=valid_rel_dirs).delete()

        return {
            "created_folders": created_folders,
            "created_files": created_files,
            "deleted_files": deleted_files
        }