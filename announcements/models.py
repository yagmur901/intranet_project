from django.db import models

class Announcement(models.Model):
    title = models.CharField(max_length=200, verbose_name="Duyuru Başlığı")
    content = models.TextField(verbose_name="Duyuru İçeriği")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Son Güncellenme") # kayıt güncellendiğinde değişir, yoksa created_at ile aynı olur

    class Meta:
        ordering = ['-updated_at'] # azalan updated_at sıralaması (daha güncellenmediyse, updated_at = created_at)
        verbose_name = "Duyuru"
        verbose_name_plural = "Duyurular"

    def __str__(self):
        return self.title