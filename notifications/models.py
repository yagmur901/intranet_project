from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255, verbose_name="Başlık")
    message = models.TextField(blank=True, null=True, verbose_name="Mesaj")
    link = models.CharField(max_length=255, blank=True, null=True, verbose_name="Yönlendirme Linki")
    is_read = models.BooleanField(default=False, verbose_name="Okundu mu?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Bildirim"
        verbose_name_plural = "Bildirimler"

    def __str__(self):
        return f"{self.user.username} - {self.title}"