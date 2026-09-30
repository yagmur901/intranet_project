from django.shortcuts import redirect
from django.conf import settings
from django.contrib import messages
from dashboard.models import DashboardSettings

class GlobalLoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # herkese açık olması gereken pathler (giriş sayfası, admin girişi ve statik dosyalar)
        allowed_paths = [settings.LOGIN_URL, '/admin/login/']
        
        # eğer kullanıcı giriş yapmamışsa ve girmeye çalıştığı yer serbest bölge değilse:
        if not request.user.is_authenticated:
            if not any(request.path.startswith(path) for path in allowed_paths) and not request.path.startswith('/static/'):
                return redirect(settings.LOGIN_URL)
                
        return self.get_response(request)


class ModuleAccessMiddleware:
    """
    Admin panelinden kapatılan modüllerin URL'lerine (bildirimden, aramadan veya doğrudan) 
    erişilmeye çalışıldığında hata vermek yerine uyarı verip anasayfaya yönlendirir.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # hangi URL uzantısı hangi ayara bağlı
        self.module_rules = [
            ('/tickets', 'show_tickets', 'IT Destek'),
            ('/documents', 'show_documents', 'Doküman Merkezi'),
            ('/events', 'show_calendar', 'Etkinlik Takvimi'),
            ('/announcements', 'show_announcements', 'Duyurular'),
            ('/trainings', 'show_training', 'Eğitimler'),
            ('/employees', 'show_employees', 'Personel Rehberi'),
            ('/workspace', 'show_workspaces', 'Çalışma Alanı'),
        ]

    def __call__(self, request):
        path = request.path

        # Admin paneline, statik ve medya dosyalarına her zaman izin ver
        if path.startswith('/admin') or path.startswith('/static') or path.startswith('/media'):
            return self.get_response(request)

        dashboard_settings = DashboardSettings.objects.first()
        if dashboard_settings:
            for url_prefix, setting_field, module_name in self.module_rules:
                if path.startswith(url_prefix):
                    # Ayar kapalı ise erişimi engelle ve anasayfaya yönlendir
                    if getattr(dashboard_settings, setting_field, True) is False:
                        messages.warning(request, f"{module_name} modülü şu anda geçici olarak kullanım dışıdır.")
                        return redirect('/')

        return self.get_response(request)