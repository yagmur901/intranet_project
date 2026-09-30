from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Ekleyen Kullanıcı")
    is_corporate = models.BooleanField(default=True, verbose_name="Kurumsal Etkinlik (Herkese Açık)")
    title = models.CharField(max_length=200, verbose_name="Etkinlik Başlığı")
    description = models.TextField(blank=True, null=True, verbose_name="Açıklama")
    start_date = models.DateTimeField(verbose_name="Başlangıç Tarihi ve Saati")
    end_date = models.DateTimeField(blank=True, null=True, verbose_name="Bitiş Tarihi ve Saati")
    location = models.CharField(max_length=150, verbose_name="Konum / Link", blank=True, null=True)

    class Meta:
        verbose_name = "Etkinlik"
        verbose_name_plural = "Etkinlikler"

    def __str__(self):
        return f"{self.title} - {self.start_date.strftime('%d.%m.%Y')}"