from django.contrib import admin
from .models import VpsServer


@admin.register(VpsServer)
class VpsServerAdmin(admin.ModelAdmin):
    list_display = ("code", "friendly_name", "provider", "package", "main_ip", "is_active")
    list_filter = ("provider", "is_active", "package")
    search_fields = ("code", "friendly_name", "main_ip", "hostname", "domain")
    prepopulated_fields = {"slug": ("code",)}
