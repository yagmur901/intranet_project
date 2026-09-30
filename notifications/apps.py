from django.apps import AppConfig

class NotificationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notifications'
    verbose_name = "Bildirimler"  # Django admin interface

    def ready(self):
        # uygulama ayağa kalktığında merkezi bildirim sinyallerini çalıştır
        import notifications.signals