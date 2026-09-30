from django.db import models

class DashboardSettings(models.Model):
    show_quick_links = models.BooleanField(default=True, verbose_name="Hızlı Bağlantılar")
    show_announcements = models.BooleanField(default=True, verbose_name="Güncel Duyurular")
    show_training = models.BooleanField(default=True, verbose_name="Ayın Eğitimi")
    show_weather = models.BooleanField(default=True, verbose_name="Hava Durumu")
    show_calendar = models.BooleanField(default=True, verbose_name="Mini Takvim")
    show_feedback = models.BooleanField(default=True, verbose_name="Geri Bildirim")
    show_documents = models.BooleanField(default=True, verbose_name="Son Dokümanlar")
    show_tickets = models.BooleanField(default=True, verbose_name="Son Destek Talepleri")

    show_employees = models.BooleanField(default=True, verbose_name="Personel Rehberi")
    show_workspaces = models.BooleanField(default=True, verbose_name="Çalışma Alanı")

    class Meta:
        verbose_name = "Pano Ayarı"
        verbose_name_plural = "Pano Ayarları"

    def __str__(self):
        return "Ana Sayfa Modül Ayarları"