from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Event, Ticket

class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'role', 'date_joined']

class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'date', 'total_tickets', 'tickets_sold']

class TicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'quantity', 'purchase_date', 'event_id', 'user_id']

admin.site.register(User, UserAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Ticket, TicketAdmin)
