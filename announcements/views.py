from django.shortcuts import render, get_object_or_404
from .models import Announcement
from django.core.paginator import Paginator
import requests # API çağrıları için eklendi
from datetime import datetime



def announcement_list_view(request):
    # veritabanındaki tüm duyurular çekilir (models.py'daki kuralla zaten sıralı geliyor)
    announcement_list = Announcement.objects.all()
    
    # tüm duyurular 10'arlı sayfalara bölünür
    paginator = Paginator(announcement_list, 10) 

    # kullanıcı hangi sayfada
    page_number = request.GET.get('page')
    
    # ilgili sayfanın paketi
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'announcements_list.html', {'page_obj': page_obj})



def announcement_detail_view(request, id):
    # idye göre duyuruyu bulur, eğer o id yoksa 404 sayfası verir
    announcement = get_object_or_404(Announcement, id=id)
    return render(request, 'announcement_detail.html', {'announcement': announcement})