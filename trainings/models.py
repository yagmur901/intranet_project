from django.db import models

class MonthlyTraining(models.Model):
    title = models.CharField(max_length=200, verbose_name="Eğitim Başlığı")
    description = models.TextField(verbose_name="Açıklama")
    url = models.URLField(verbose_name="Eğitim Linki (URL)")
    is_active = models.BooleanField(default=True, verbose_name="Aktif mi?")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Ayın Eğitimi"
        verbose_name_plural = "Ayın Eğitimleri"

    def __str__(self):
        return self.title