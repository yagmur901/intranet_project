from django.db import models

class Employee(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Ad")
    last_name = models.CharField(max_length=100, verbose_name="Soyad")
    short_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Kısa İsim")
    department = models.CharField(max_length=100, blank=True, null=True, verbose_name="Departman")
    
    # Benzersiz Yapılan Alanlar:
    email = models.EmailField(unique=True, blank=True, null=True, verbose_name="E-posta")
    phone_number = models.CharField(max_length=20, unique=True, blank=True, null=True, verbose_name="Telefon")

    class Meta:
        verbose_name = "Personel"
        verbose_name_plural = "Personeller"
        ordering = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip() or "İsimsiz Personel"