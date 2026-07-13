from django.contrib import admin
from .models import BookingRequest

@admin.register(BookingRequest)
class BookingRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'service_type', 'preferred_date', 'status', 'created_at')
    list_filter = ('service_type', 'status', 'preferred_date')
    search_fields = ('name', 'email', 'phone')
