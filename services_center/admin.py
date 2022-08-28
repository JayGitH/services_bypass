from django.contrib import admin
from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'server_name', 'server_host', 'server_port')

