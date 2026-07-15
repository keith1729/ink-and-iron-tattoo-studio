from django.contrib import admin
from django.utils.html import format_html
from .models import BookingRequest, TattooImage, Artist

@admin.register(BookingRequest)
class BookingRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'service_type', 'preferred_date', 'status', 'created_at')
    list_filter = ('service_type', 'status', 'preferred_date')
    search_fields = ('name', 'email', 'phone')

@admin.register(TattooImage)
class TattooImageAdmin(admin.ModelAdmin):
    list_display = ('thumbnail', 'title', 'uploaded_at')
    list_display_links = ('title',)

    def thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height: 60px; width: 60px; object-fit: cover; border-radius: 4px;" />',
                obj.image.url,
            )
        return "No image"
    thumbnail.short_description = 'Preview'

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('thumbnail', 'name', 'specialty', 'order')
    list_display_links = ('name',)
    list_editable = ('order',)

    def thumbnail(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="height: 50px; width: 50px; object-fit: cover; border-radius: 50%;" />',
                obj.photo.url,
            )
        return "No photo"
    thumbnail.short_description = 'Photo'