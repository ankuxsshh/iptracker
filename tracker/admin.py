from django.contrib import admin
from .models import VisitorLog

@admin.register(VisitorLog)
class VisitorLogAdmin(admin.ModelAdmin):
    list_display = ("ip", "city", "region", "country", "isp", "latitude", "longitude", "timestamp")
    list_filter = ("country", "region")
    search_fields = ("ip", "city", "region", "country", "isp")
