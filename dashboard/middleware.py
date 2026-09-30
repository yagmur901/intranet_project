from django.http import Http404
from .models import DashboardSettings

class ModuleAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Adminin belirlediği ayarları çek
        settings = DashboardSettings.objects.first()
        
        if settings:
            path = request.path
            
            # Eğer kullanıcı /tickets/ linkine gitmeye çalışıyorsa ve biletler kapalıysa:
            if path.startswith('/tickets/') and not settings.show_tickets:
                raise Http404("Destek Talepleri modülü geçici olarak kullanıma kapatılmıştır.")
            
        # Bir sorun yoksa kullanıcının gitmek istediği sayfayı aç
        response = self.get_response(request)
        return response