
"""clinic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import include, path
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin

urlpatterns = [
    path('admin/', admin.site.urls, name = 'admin'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('home/', TemplateView.as_view(template_name='home.html'), name='home'),
    path('doctor_interface/', include('doctor_interface.urls'), name='doctor_interface'),
    path('reception_desk/', include('reception_desk.urls'), name='reception_desk'),
    url('^', include('django.contrib.auth.urls')),
]

admin.site.unregister(Group)
admin.site.unregister(User)
UserAdmin.fieldsets = [
        (None,               {'fields': ['email', 'password']}),
        ('Personal Info', {'fields': ['first_name', 'last_name']}),
        ('Important Dates', {'fields': ['last_login', 'date_joined']}),
    ]
admin.site.register(User, UserAdmin)
