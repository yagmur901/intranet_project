from django.shortcuts import render, redirect
from datetime import datetime
import calendar
import requests
from django.utils import timezone
from announcements.models import Announcement
from events.models import Event
from documents.models import Document
from tickets.models import Ticket
from trainings.models import MonthlyTraining
from django.db.models import Q
from django.http import JsonResponse
from employees.models import Employee
from dashboard.models import DashboardSettings
from workspace.models import WorkspaceFolder, WorkspaceFile

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

from django.contrib.auth.decorators import login_required

def home_view(request):

    settings = DashboardSettings.objects.first()
    if not settings:
        # admin panelinden henüz ayar kaydedilmediyse varsayılan olarak her şeyi açık kabul et
        class DummySettings:
            show_quick_links = True
            show_announcements = True
            show_training = True
            show_weather = True
            show_calendar = True
            show_feedback = True
            show_documents = True
            show_tickets = True
        settings = DummySettings()

    recent_announcements = []
    weather_data = None
    calendar_weeks = []
    upcoming_events = []
    active_training = None
    recent_documents = []
    recent_tickets = []

    now = timezone.now()
    year = now.year
    month = now.month
    today_day = now.day
    turkish_months = [
        "", "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
        "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"
    ]
    current_month_name = turkish_months[month]

    # ayarlara bağlı sorgular

    if settings.show_announcements:
        recent_announcements = Announcement.objects.all().order_by('-created_at')[:7]

    if settings.show_training:
        active_training = MonthlyTraining.objects.filter(is_active=True).first()

    if settings.show_documents:
        recent_documents = Document.objects.all().order_by('-created_at')[:3]

    if settings.show_tickets:
        if request.user.is_authenticated:
            recent_tickets = Ticket.objects.filter(user=request.user).order_by('-created_at')[:3]

    if settings.show_weather:
        try:
            w_url = "https://api.open-meteo.com/v1/forecast?latitude=39.92&longitude=32.85&current=temperature_2m,relative_humidity_2m,wind_speed_10m,precipitation&daily=sunrise,sunset,uv_index_max&timezone=Europe%2FIstanbul"
            a_url = "https://air-quality-api.open-meteo.com/v1/air-quality?latitude=39.92&longitude=32.85&current=european_aqi,grass_pollen&timezone=Europe%2FIstanbul"
            
            w_resp = requests.get(w_url, timeout=3).json()
            a_resp = requests.get(a_url, timeout=3).json()
            
            temp = w_resp['current']['temperature_2m']
            humidity = w_resp['current']['relative_humidity_2m']
            wind = w_resp['current']['wind_speed_10m']
            precip = w_resp['current']['precipitation']
            
            uv = w_resp['daily']['uv_index_max'][0]
            sunrise = datetime.fromisoformat(w_resp['daily']['sunrise'][0]).strftime('%H:%M')
            sunset = datetime.fromisoformat(w_resp['daily']['sunset'][0]).strftime('%H:%M')
            
            aqi = a_resp['current']['european_aqi']
            pollen = a_resp['current']['grass_pollen']
            
            if 10 <= temp <= 25 and humidity < 70 and precip == 0 and aqi < 60:
                run_cond = "İyi (Uygun)"
                run_color = "text-green-300"
            elif temp > 30 or temp < 5 or precip > 0 or aqi > 100:
                run_cond = "Kötü (Önerilmez)"
                run_color = "text-red-300"
            else:
                run_cond = "Orta (Dikkatli Olun)"
                run_color = "text-yellow-300"

            weather_data = {
                'temp': round(temp), 'humidity': humidity, 'wind': wind, 'uv': uv,
                'sunrise': sunrise, 'sunset': sunset, 'aqi': aqi, 'pollen': round(pollen, 1),
                'run_cond': run_cond, 'run_color': run_color
            }
        except Exception as e:
            print(f"Weather API Error: {e}")
            pass

    if settings.show_calendar:
        month_events = Event.objects.filter(start_date__year=year, start_date__month=month)
        event_days = set(month_events.values_list('start_date__day', flat=True))

        cal = calendar.Calendar(firstweekday=0)
        month_days = cal.monthdayscalendar(year, month)

        for week in month_days:
            week_data = []
            for day in week:
                week_data.append({
                    'day': day,
                    'is_today': (day == today_day),
                    'has_event': (day in event_days)
                })
            calendar_weeks.append(week_data)

        upcoming_events = Event.objects.filter(start_date__gte=now).order_by('start_date')[:2]

    # tüm verileri ve ayarları HTML'e gönder
    context = {
        'settings': settings,
        'announcements': recent_announcements,
        'weather': weather_data,
        'events': upcoming_events,
        'calendar_weeks': calendar_weeks,
        'current_month_name': current_month_name,
        'current_year': year,
        'recent_documents': recent_documents,
        'recent_tickets': recent_tickets,
        'active_training': active_training,
    }
    return render(request, 'home.html', context)

# Ayar Kontrollü
SEARCH_MODULES = [
    {
        'model': Employee,
        'search_fields': ['first_name', 'last_name', 'department', 'email'],
        'type_name': 'Personel Rehberi',
        'icon': 'fa-user-tie',
        'url_name': '/employees/',
        'setting_field': 'show_employees' # Modelde yoksa varsayılan açık kabul edilir
    },
    {
        'model': Document,
        'search_fields': ['title', 'description'],
        'type_name': 'Doküman Merkezi',
        'icon': 'fa-folder-open',
        'url_name': '/documents/',
        'setting_field': 'show_documents'
    },
    {
        'model': Ticket,
        'search_fields': ['title', 'description'],
        'type_name': 'IT Destek',
        'icon': 'fa-headset',
        'url_name': '/tickets/',
        'setting_field': 'show_tickets'
    },
    {
        'model': MonthlyTraining,
        'search_fields': ['title', 'description'],
        'type_name': 'Eğitimler',
        'icon': 'fa-graduation-cap',
        'url_name': '/trainings/',
        'setting_field': 'show_training'
    },
    {
        'model': Announcement,
        'search_fields': ['title', 'content'],
        'type_name': 'Duyurular',
        'icon': 'fa-bullhorn',
        'url_name': '/announcements/',
        'setting_field': 'show_announcements'
    },
    {
        'model': Event,
        'search_fields': ['title', 'description'],
        'type_name': 'Etkinlikler',
        'icon': 'fa-calendar-days',
        'url_name': '/events/',
        'setting_field': 'show_calendar'
    },
    {
        'model': WorkspaceFile,
        'search_fields': ['title'],
        'type_name': 'Çalışma Dosyası',
        'icon': 'fa-file-lines',
        'url_name': '/workspace/',
        'setting_field': 'show_workspaces'
    },
    {
        'model': WorkspaceFolder,
        'search_fields': ['name'],
        'type_name': 'Çalışma Klasörü',
        'icon': 'fa-folder-tree',
        'url_name': '/workspace/',
        'setting_field': 'show_workspaces'
    }
]


def is_module_active(setting_field):
    """Verilen modülün DashboardSettings'te açık olup olmadığını kontrol eder."""
    if not setting_field:
        return True
    settings = DashboardSettings.objects.first()
    if not settings:
        return True
    # Eğer ayarlar modelinde bu alan varsa değerini döndür, yoksa açık kabul et
    return getattr(settings, setting_field, True)

def build_search_query(query, fields):
    """
    Verilen alanlar için arama mantığını (OR) dinamik olarak oluşturur.
    """
    search_q = Q()
    for field in fields:
        search_q |= Q(**{f"{field}__icontains": query})
    return search_q

def get_item_search_url(item, module, query=""):
    """
    Arama sonucunda çıkan her bir öğe için nokta atışı yönlendirme URL'i üretir.
    """
    model_cls = module['model']
    base_url = module['url_name']

    # Doküman ise: Sadece o dokümanın listeleneceği doc_id parametresiyle gönder
    if model_cls == Document:
        return f"{base_url}?doc_id={item.id}"
    
    # Bilet veya Duyuru ise: Doğrudan kendi detay sayfasına gönder
    elif model_cls in [Ticket, Announcement]:
        return f"{base_url}{item.id}/"
    
    # Etkinlik ise: Etkinliğin olduğu tarihe göre takvime gönder
    elif model_cls == Event and getattr(item, 'start_date', None):
        d = item.start_date
        return f"{base_url}?date={d.year}-{d.month}-{d.day}"
    
    # Eğitim ise ve url varsa oraya, yoksa ana sayfaya
    elif model_cls == MonthlyTraining:
        return getattr(item, 'url', '/') or '/'
    
    # Personel veya Çalışma Alanı ise: Arama sorgusuyla birlikte gönder
    elif model_cls in [Employee, WorkspaceFile, WorkspaceFolder] and query:
        return f"{base_url}?q={query}"

    return base_url

def global_search(request):
    query = request.GET.get('q', '').strip()
    results = {}
    error_message = None

    if query:
        if len(query) < 2:
            error_message = "Lütfen arama yapmak için en az 2 karakter girin."
        else:
            for module in SEARCH_MODULES:
                # Modül admin panelinden kapatılmışsa aramaya dahil etme
                if not is_module_active(module.get('setting_field')):
                    continue

                q_objects = build_search_query(query, module['search_fields'])
                module_results = list(module['model'].objects.filter(q_objects).distinct())
                
                if module_results:
                    for item in module_results:
                        item.target_url = get_item_search_url(item, module, query)

                    results[module['type_name']] = {
                        'icon': module['icon'],
                        'url': module['url_name'],
                        'items': module_results
                    }

    return render(request, 'search_results.html', {
        'query': query,
        'results': results,
        'error_message': error_message
    })

def live_search_api(request):
    query = request.GET.get('q', '').strip()
    data = []
    
    if len(query) >= 2:
        for module in SEARCH_MODULES:
            # Modül admin panelinden kapatılmışsa canlı aramada çıkarma
            if not is_module_active(module.get('setting_field')):
                continue

            q_objects = build_search_query(query, module['search_fields'])
            items = module['model'].objects.filter(q_objects).distinct()[:3]
            
            for item in items:
                if hasattr(item, 'first_name') and hasattr(item, 'last_name'):
                    title = f"{item.first_name} {item.last_name}"
                else:
                    title = getattr(item, 'title', None) or str(item)                
                
                data.append({
                    'type': module['type_name'],
                    'icon': module['icon'],
                    'title': title,
                    'subtitle': "Sistem Kaydı",
                    'url': get_item_search_url(item, module, query)
                })
                
    return JsonResponse(data, safe=False)

def custom_404(request, exception):
    return render(request, '404.html', status=404)



@login_required
def profile_view(request):
    if request.method == 'POST':
        # Sadece admin bu bilgileri güncelleyebilir
        if not request.user.is_superuser:
            messages.error(request, "Bu bilgileri değiştirme yetkiniz bulunmuyor. Lütfen IT departmanı ile görüşün.")
            return redirect('profile')

        # Formdan gelen verileri al
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        
        # Kullanıcı bilgilerini güncelle
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        
        messages.success(request, 'Kişisel bilgiler başarıyla güncellendi.')
        return redirect('profile')
        
    return render(request, 'profile.html', {'user': request.user})


@login_required
def settings_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # şifre değiştiğinde oturumun kapanmaması için hash güncellenir
            update_session_auth_hash(request, user)
            messages.success(request, 'Şifreniz başarıyla güncellendi.')
            return redirect('settings')
        else:
            messages.error(request, 'Lütfen aşağıdaki hataları düzeltin.')
    else:
        form = PasswordChangeForm(request.user)
        
    return render(request, 'settings.html', {'form': form})