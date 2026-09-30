from dashboard.models import DashboardSettings

def ticket_system_status(request):
    settings = DashboardSettings.objects.first()
    # dashboard_settings ki üst menüde her modülü kontrol edebilebilsin
    return {'dashboard_settings': settings}