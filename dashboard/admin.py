from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import DashboardSettings

class DashboardSettingsAdminForm(forms.ModelForm):
    # Veritabanına kaydedilmeyen, sadece arayüzde tümünü kontrol eden sanal kutu
    select_all = forms.BooleanField(
        label=mark_safe('<strong style="color: #b91c1c;">⚡ Tüm Modülleri Seç / Kaldır</strong>'),
        required=False,
        help_text="Tek tıkla tüm modülleri aktif edebilir veya devre dışı bırakabilirsiniz."
    )

    class Meta:
        model = DashboardSettings
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Sayfa ilk açıldığında eğer tüm modüller True ise "Tümünü Seç" kutusu da otomatik tikli gelsin
        if self.instance and self.instance.pk:
            model_fields = [f.name for f in DashboardSettings._meta.fields if f.name.startswith('show_')]
            self.fields['select_all'].initial = all(getattr(self.instance, f) for f in model_fields)

@admin.register(DashboardSettings)
class DashboardSettingsAdmin(admin.ModelAdmin):
    form = DashboardSettingsAdminForm
    
    # Kutucukların sırası (En üstte Tümünü Seç yer alır)
    fields = (
        'select_all',
        'show_quick_links',
        'show_announcements',
        'show_training',
        'show_weather',
        'show_calendar',
        'show_feedback',
        'show_documents',
        'show_tickets',
        'show_employees',
        'show_workspaces',
    )

    def render_change_form(self, request, context, *args, **kwargs):
        # Harici JS dosyası oluşturmaya gerek kalmadan çalışan küçük script
        response = super().render_change_form(request, context, *args, **kwargs)
        js_script = """
        <script>
        document.addEventListener('DOMContentLoaded', function() {
            const selectAll = document.getElementById('id_select_all');
            const checkboxes = document.querySelectorAll('input[type="checkbox"][id^="id_show_"]');
            
            if (selectAll) {
                // 1. "Tümünü Seç"e basıldığında diğer hepsini değiştir
                selectAll.addEventListener('change', function() {
                    checkboxes.forEach(cb => cb.checked = selectAll.checked);
                });
                
                // 2. Alttaki kutulardan biri bile kapatılırsa "Tümünü Seç" tikini kaldır, hepsi açılırsa tikle
                checkboxes.forEach(cb => {
                    cb.addEventListener('change', function() {
                        selectAll.checked = Array.from(checkboxes).every(c => c.checked);
                    });
                });
            }
        });
        </script>
        """
        response.render()
        response.content = response.content.replace(b'</body>', js_script.encode('utf-8') + b'</body>')
        return response

    # Admin panelinde yanlışlıkla 2. bir ayar objesi oluşturulmasını engeller
    def has_add_permission(self, request):
        if DashboardSettings.objects.exists():
            return False
        return super().has_add_permission(request)