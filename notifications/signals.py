from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from tickets.models import Ticket
from documents.models import Document
from events.models import Event

from .utils import send_notification
from dashboard.models import DashboardSettings


# IT destek bildirimleri 
@receiver(pre_save, sender=Ticket)
def ticket_status_handler(sender, instance, **kwargs):
    """Bilet durumu güncellendiğinde tetiklenir"""
    
    if not is_active('show_tickets'):
        return

    if not instance.pk:
        return 
    
    try:
        old_ticket = Ticket.objects.get(pk=instance.pk)
        if old_ticket.status != instance.status:
            baslik = "Talebiniz Güncellendi"
            if instance.status == 'İşlemde': baslik = "Talebiniz İşleme Alındı"
            if instance.status == 'Kapalı': baslik = "Destek Talebiniz Kapatıldı"
                
            send_notification(
                user=instance.user,
                title=baslik,
                message=f"'{instance.title}' başlıklı biletinizin durumu '{instance.status}' olarak değiştirildi.",
                link=f"/tickets/{instance.id}/"
            )
    except Ticket.DoesNotExist:
        pass

@receiver(post_save, sender=Ticket)
def ticket_created_handler(sender, instance, created, **kwargs):
    """Yeni bilet oluşturulduğunda tetiklenir"""
    if not is_active('show_tickets'):
        return
    
    if created:
        send_notification(
            user=instance.user,
            title="Destek Talebi Oluşturuldu",
            message=f"'{instance.title}' başlıklı talebiniz IT ekibine iletilmek üzere kaydedildi.",
            link=f"/tickets/{instance.id}/"
        )



# Doküman bildirimleri
@receiver(post_save, sender=Document)
def document_upload_handler(sender, instance, created, **kwargs):
    """Yeni doküman yüklendiğinde tüm personele bildirim atar"""
    if not is_active('show_documents'):
        return

    if created:
        # Tüm aktif kullanıcıları buluyoruz
        users = User.objects.filter(is_active=True)
        for user in users:
            send_notification(
                user=user,
                title="Yeni Kurumsal Doküman",
                message=f"Sisteme yeni bir doküman eklendi: {instance.title}",
                link=f"/documents/?doc_id={instance.id}"
            )



# Etkinlik takvimi bildirimleri
@receiver(post_save, sender=Event)
def event_saved_handler(sender, instance, created, **kwargs):
    if not is_active('show_calendar'):
        return

    # sadece kurumsal etkinliklerde herkese bildirim gider.
    if instance.is_corporate:
        users = User.objects.filter(is_active=True)
        tarih = instance.start_date.strftime('%d.%m.%Y %H:%M') if instance.start_date else ""
        link_str = f"/events/?date={instance.start_date.strftime('%Y-%m-%d')}"
        
        if created:
            title = "Yeni Şirket Etkinliği"
            message = f"{tarih} tarihinde '{instance.title}' planlandı."
        else:
            title = "Kurumsal Etkinlik Güncellendi"
            message = f"'{instance.title}' etkinliğinin detaylarında veya tarihinde değişiklik yapıldı."
            
        for user in users:
            # düzenleyen kişinin kendisine bildirim atmasını engelle
            if user != instance.user:
                send_notification(user=user, title=title, message=message, link=link_str)
                

def is_active(field_name):
    s = DashboardSettings.objects.first()
    return getattr(s, field_name, True) if s else True