from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Ticket
from .forms import TicketForm

@login_required
def ticket_list_view(request):
    # Sadece giriş yapan kişinin biletlerini getir
    tickets = Ticket.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'tickets/ticket_list.html', {'tickets': tickets})

@login_required
def ticket_create_view(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user  # Bileti oluşturan kişiyi otomatik ata
            ticket.status = 'Açık'      # Yeni açılan biletin varsayılan durumu
            ticket.save()               # post_save sinyali
            
            messages.success(request, "Destek talebiniz başarıyla oluşturuldu!")
            return redirect('ticket_list')    
    else:
        form = TicketForm()
        
    return render(request, 'tickets/ticket_form.html', {'form': form})

@login_required
def ticket_detail_view(request, ticket_id):
    # Adminler (IT) tüm biletleri görebilsin, normal personel sadece kendi biletini görebilsin
    if request.user.is_staff:
        ticket = get_object_or_404(Ticket, id=ticket_id)
    else:
        ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)
        
    return render(request, 'tickets/ticket_detail.html', {'ticket': ticket})

# IT veya Yetkili Personelin Bilet Durumunu Güncellemesi
@login_required
def ticket_update_status(request, ticket_id):
    # Sadece yetkililer (is_staff) durumu güncelleyebilir
    if not request.user.is_staff:
        return redirect('ticket_list')

    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == 'POST':
        yeni_durum = request.POST.get('status') 
        
        if yeni_durum in ['Açık', 'İşlemde', 'Kapalı'] and ticket.status != yeni_durum:
            ticket.status = yeni_durum
            ticket.save()               # pre_save sinyali
            
            messages.success(request, f"Bilet durumu başarıyla '{yeni_durum}' olarak güncellendi.")

    return redirect('ticket_detail', ticket_id=ticket.id)