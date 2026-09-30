from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Notification
from dashboard.models import DashboardSettings

def filter_active_notifications(queryset):
    """Kapalı olan modüllere ait bildirimleri listeden geçici olarak gizler."""
    settings = DashboardSettings.objects.first()
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

@login_required
def notification_list(request):
    # Kullanıcının bildirimlerini getir ve kapalı modülleri filtrele
    notifications = Notification.objects.filter(user=request.user)
    notifications = filter_active_notifications(notifications)
    return render(request, 'notification_list.html', {'notifications': notifications})

@login_required
def mark_all_as_read(request):
    # Sadece aktif olan okunmamış bildirimleri okundu yap
    unread_qs = Notification.objects.filter(user=request.user, is_read=False)
    active_unread_ids = filter_active_notifications(unread_qs).values_list('id', flat=True)
    Notification.objects.filter(id__in=list(active_unread_ids)).update(is_read=True)
    
    # Geldiği sayfaya geri döndür
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def read_and_redirect(request, notif_id):
    # Bildirime tıklandığında hem okundu yap hem de ilgili linke yönlendir
    notif = get_object_or_404(Notification, id=notif_id, user=request.user)
    notif.is_read = True
    notif.save()
    
    if notif.link:
        return redirect(notif.link)
    return redirect('notifications:list')