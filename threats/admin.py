from django.contrib import admin
from .models import Event, Alert


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'source_name', 'event_type', 'severity', 'timestamp')
    list_filter = ('severity', 'event_type')
    search_fields = ('source_name', 'event_type', 'description')
    ordering = ('-timestamp',)


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('id', 'event', 'status', 'created_at')
    list_filter = ('status', 'event__severity')
    search_fields = ('event__source_name',)
    ordering = ('-created_at',)
