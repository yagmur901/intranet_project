from django.db import models
from django.contrib.auth.models import User


# IT Destek Talebi
class Ticket(models.Model):
    STATUS_CHOICES = (
        ('acik', 'Açık'),
        ('islemde', 'İşlemde'),
        ('kapali', 'Kapalı'),
    )
    PRIORITY_CHOICES = (
        ('dusuk', 'Düşük'),
        ('normal', 'Normal'),
        ('acil', 'Acil'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Personel")
    title = models.CharField(max_length=200, verbose_name="Sorun Başlığı")
    description = models.TextField(verbose_name="Sorun Detayı")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='acik', verbose_name="Durum")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='normal', verbose_name="Öncelik")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Destek Talebi"
        verbose_name_plural = "Destek Talepleri"

    def __str__(self):
        return f"{self.title} - {self.user.username}"
    















