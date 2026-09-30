from .models import Notification

def send_notification(user, title, message="", link=""):
    """
    Sistemin herhangi bir yerinden bildirim oluşturmayı sağlayan yardımcı fonksiyon.
    send_notification(user_obj, "Bilet Güncellendi", "Talebiniz çözüldü.", "/tickets/1/")
    """
    Notification.objects.create(
        user=user,
        title=title,
        message=message,
        link=link
    )