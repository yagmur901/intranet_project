from django.db import models
import os

class DocumentCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Kategori Adı")
    description = models.TextField(blank=True, null=True, verbose_name="Açıklama")

    class Meta:
        verbose_name = "Doküman Kategorisi"
        verbose_name_plural = "Doküman Kategorileri"

    def __str__(self):
        return self.name

class Document(models.Model):
    title = models.CharField(max_length=200, verbose_name="Belge Başlığı")
    category = models.ForeignKey(DocumentCategory, on_delete=models.CASCADE, related_name='documents', verbose_name="Kategori")
    file = models.FileField(upload_to='documents/%Y/%m/', verbose_name="Dosya")
    description = models.TextField(blank=True, null=True, verbose_name="Açıklama")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yüklenme Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Son Güncelleme")

    class Meta:
        verbose_name = "Doküman"
        verbose_name_plural = "Dokümanlar"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def file_extension(self):
        """Dosya uzantısını döner (.pdf, .docx, .xlsx vb.)"""
        name, extension = os.path.splitext(self.file.name)
        return extension.lower().replace('.', '')

    @property
    def file_size(self):
        """Dosya boyutunu KB veya MB cinsinden okunabilir döner"""
        try:
            bytes_size = self.file.size
            if bytes_size >= 1048576:
                return f"{bytes_size / 1048576:.1f} MB"
            return f"{bytes_size / 1024:.0f} KB"
        except Exception:
            return "Bilinmiyor"

