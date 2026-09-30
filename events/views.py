from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import datetime, timedelta
import calendar
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Event
from django.shortcuts import get_object_or_404


@login_required
def event_calendar_view(request):
    now = timezone.now()
    
    # Sadece Kurumsal etkinlikler veya kullanıcının kendi eklediği etkinlikler görünür
    event_query = Q(is_corporate=True) | Q(user=request.user)
    
    # URLden date parametresi gelmiş mi kontrol etü
    date_str = request.GET.get('date')
    if date_str:
        try:
            current_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            current_date = now.date()
            
        prev_day = current_date - timedelta(days=1)
        next_day = current_date + timedelta(days=1)

        day_events = Event.objects.filter(event_query).filter(
            start_date__year=current_date.year,
            start_date__month=current_date.month,
            start_date__day=current_date.day
        ).order_by('start_date')

        months_tr = ["", "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
        days_tr = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
        formatted_date_str = f"{current_date.day} {months_tr[current_date.month]} {current_date.year}, {days_tr[current_date.weekday()]}"

        context = {
            'current_date': current_date,
            'formatted_date': formatted_date_str,
            'prev_date': prev_day.strftime('%Y-%m-%d'),
            'next_date': next_day.strftime('%Y-%m-%d'),
            'day_events': day_events,
        }
        return render(request, 'events/event_day_detail.html', context)

    # Tarih parametresi yoksa Aylık Takvim
    year = int(request.GET.get('year', now.year))
    month = int(request.GET.get('month', now.month))
    
    prev_month = 12 if month == 1 else month - 1
    prev_year = year - 1 if month == 1 else year
        
    next_month = 1 if month == 12 else month + 1
    next_year = year + 1 if month == 12 else year

    # Seçili ayın filtrelenmiş etkinlikleri
    events = Event.objects.filter(event_query).filter(
        start_date__year=year,
        start_date__month=month
    ).order_by('start_date')
    
    events_by_day = {}
    for ev in events:
        day_num = ev.start_date.day
        events_by_day.setdefault(day_num, []).append(ev)

    cal = calendar.Calendar(firstweekday=0)
    month_matrix = cal.monthdayscalendar(year, month)

    calendar_weeks = []
    today = now.date()
    
    for week in month_matrix:
        week_data = []
        for day in week:
            day_events = events_by_day.get(day, []) if day != 0 else []
            is_today = (day == today.day and month == today.month and year == today.year)
            week_data.append({
                'day': day,
                'is_today': is_today,
                'events': day_events,
            })
        calendar_weeks.append(week_data)

    turkish_months = [(1, "Ocak"), (2, "Şubat"), (3, "Mart"), (4, "Nisan"), (5, "Mayıs"), (6, "Haziran"), (7, "Temmuz"), (8, "Ağustos"), (9, "Eylül"), (10, "Ekim"), (11, "Kasım"), (12, "Aralık")]
    current_month_name = dict(turkish_months)[month]
    years_range = list(range(now.year - 4, now.year + 5))

    context = {
        'calendar_weeks': calendar_weeks,
        'current_month_name': current_month_name,
        'current_year': year,
        'current_month': month,
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
        'today_year': today.year,
        'today_month': today.month,
        'turkish_months': turkish_months,
        'years_range': years_range,
    }
    return render(request, 'events/event_calendar.html', context)


@login_required
def event_add_view(request):
    if request.method == "POST":
        title = request.POST.get('title')
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        location = request.POST.get('location')
        description = request.POST.get('description')
        
        # Sadece adminler kurumsal etkinlik ekleyebilir, diğerleri kişisel etkinlik olarak kaydedilir
        is_corporate = True if (request.user.is_superuser and request.POST.get('is_corporate') == 'on') else False
        
        if title and start_date_str:
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%dT%H:%M')
                end_date = datetime.strptime(end_date_str, '%Y-%m-%dT%H:%M') if end_date_str else None
                
                Event.objects.create(
                    user=request.user,
                    is_corporate=is_corporate,
                    title=title,
                    start_date=start_date,
                    end_date=end_date,
                    location=location,
                    description=description
                )
                messages.success(request, "Etkinlik başarıyla eklendi.")
                return redirect('event_calendar')
            except ValueError:
                messages.error(request, "Geçersiz tarih/saat formatı girdiniz.")
        else:
            messages.error(request, "Lütfen gerekli alanları doldurun.")
            
    return render(request, 'events/event_add.html')



@login_required
def event_edit_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    # Sadece etkinliği oluşturan kişi veya admin düzenleyebilir
    if event.user != request.user and not request.user.is_superuser:
        messages.error(request, "Bu etkinliği düzenleme yetkiniz bulunmuyor.")
        return redirect('event_calendar')

    if request.method == "POST":
        event.title = request.POST.get('title')
        event.location = request.POST.get('location')
        event.description = request.POST.get('description')
        
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        
        try:
            event.start_date = datetime.strptime(start_date_str, '%Y-%m-%dT%H:%M')
            if end_date_str:
                event.end_date = datetime.strptime(end_date_str, '%Y-%m-%dT%H:%M')
            else:
                event.end_date = None
        except ValueError:
            messages.error(request, "Geçersiz tarih formatı.")
            return render(request, 'events/event_edit.html', {'event': event})

        # Sadece adminler kurumsal yetkiyi değiştirebilir
        if request.user.is_superuser:
            event.is_corporate = True if request.POST.get('is_corporate') == 'on' else False

        event.save()
        messages.success(request, "Etkinlik başarıyla güncellendi.")
        return redirect(f"/events/?date={event.start_date.strftime('%Y-%m-%d')}")
        
    return render(request, 'events/event_edit.html', {'event': event})

@login_required
def event_delete_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    if event.user == request.user or request.user.is_superuser:
        date_str = event.start_date.strftime('%Y-%m-%d')
        event.delete()
        messages.success(request, "Etkinlik takvimden silindi.")
        return redirect(f"/events/?date={date_str}")
    
    messages.error(request, "Bunu silme yetkiniz yok.")
    return redirect('event_calendar')