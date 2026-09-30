from django.db import models
from pathlib import Path

class WorkspaceFolder(models.Model):
    name = models.CharField(max_length=150, verbose_name="Klasör Adı")
    relative_path = models.CharField(max_length=500, unique=True, default="", verbose_name="Göreceli Yol")
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='children', 
        verbose_name="Üst Klasör"
    )

    class Meta:
        verbose_name = "Çalışma Alanı Klasörü"
        verbose_name_plural = "Çalışma Alanı Klasörleri"
        ordering = ['name']

    def __str__(self):
        return self.relative_path or self.name


class WorkspaceFile(models.Model):
    title = models.CharField(max_length=255, verbose_name="Dosya Adı")
    folder = models.ForeignKey(
        WorkspaceFolder, 
        on_delete=models.CASCADE, 
        related_name='files', 
        verbose_name="Klasör"
    )
    file_path = models.CharField(max_length=500, unique=True, verbose_name="Dosya Yolu")
    file_size_bytes = models.BigIntegerField(default=0, verbose_name="Boyut (Bayt)")
    last_modified = models.DateTimeField(null=True, blank=True, verbose_name="Son Değiştirilme")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Kayıt Tarihi")

    class Meta:
        verbose_name = "Çalışma Alanı Dosyası"
        verbose_name_plural = "Çalışma Alanı Dosyaları"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def file_extension(self):
        return Path(self.file_path).suffix.lower().replace('.', '')

    @property
    def file_size(self):
        bytes_size = self.file_size_bytes
        if bytes_size >= 1048576:
            return f"{bytes_size / 1048576:.1f} MB"
        return f"{bytes_size / 1024:.0f} KB"