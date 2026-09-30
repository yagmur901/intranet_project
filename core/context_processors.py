from notifications.models import Notification
from dashboard.models import DashboardSettings

def filter_active_notifications(queryset, settings):
    # kapalı olan modüllere ait bildirimleri çan menüsünden ve sayaçtan gizler
    if not settings:
        return queryset

    if not getattr(settings, 'show_tickets', True):
        queryset = queryset.exclude(link__startswith='/tickets')
    if not getattr(settings, 'show_documents', True):
        queryset = queryset.exclude(link__startswith='/documents')
    if not getattr(settings, 'show_calendar', True):
        queryset = queryset.exclude(link__startswith='/events')
    if not getattr(settings, 'show_workspaces', True):
        queryset = queryset.exclude(link__startswith='/workspace')
    if not getattr(settings, 'show_employees', True):
        queryset = queryset.exclude(link__startswith='/employees')
        
    return queryset

def global_notifications(request):
    settings = DashboardSettings.objects.first()
    
    # Admin panelinden henüz ayar kaydedilmediyse varsayılan olarak hepsini açık kabul et
    if not settings:
        class DummySettings:
            show_quick_links = True
            show_announcements = True
            show_training = True
            show_weather = True
            show_calendar = True
            show_feedback = True
            show_documents = True
            show_tickets = True
            show_employees = True
            show_workspaces = True
        settings = DummySettings()

    if request.user.is_authenticated:
        user_notifs = Notification.objects.filter(user=request.user)
        # kapalı modüllerin bildirimlerini filtreleme
        active_notifs = filter_active_notifications(user_notifs, settings)
        
        unread_count = active_notifs.filter(is_read=False).count()
        latest_notifications = active_notifs[:5]
        
        return {
            'unread_notifications_count': unread_count,
            'latest_notifications': latest_notifications,
            'dashboard_settings': settings,  # sayfalarda üst menü sekmelerini kontrol eder
        }
    
    return {
        'unread_notifications_count': 0,
        'latest_notifications': [],
        'dashboard_settings': settings,
    }