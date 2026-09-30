"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from announcements.views import announcement_list_view, announcement_detail_view
from django.conf import settings
from employees.views import employee_list_view
from .views import home_view
from django.conf.urls.static import static
from . import views
from core.views import profile_view, settings_view

admin.site.site_header = 'Kurumsal İntranet Sitesi Admin Paneli'
admin.site.site_title = 'İntranet Portal'
admin.site.index_title = 'Sistem Yönetimi'


urlpatterns = [ # sayfa urlleri
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),  # anasayfa
    path('announcements/', announcement_list_view, name='announcements_list'),
    path('announcements/<int:id>/', announcement_detail_view, name='announcement_detail'),
    path('employees/', employee_list_view, name='employee_list'), 
    path('events/', include('events.urls')),
    path('documents/', include('documents.urls')),
    path('workspace/', include('workspace.urls')),
    path('accounts/', include('django.contrib.auth.urls')), 
    path('workspace/', include('workspace.urls')),
    path('tickets/', include('tickets.urls')),
    path('search/', views.global_search, name='global_search'),
    path('api/search/', views.live_search_api, name='live_search_api'),
    path('notifications/', include('notifications.urls')),
    path('profile/', profile_view, name='profile'),
    path('settings/', settings_view, name='settings'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'core.views.custom_404'