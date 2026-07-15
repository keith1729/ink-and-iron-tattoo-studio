from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .forms import BookingRequestForm
from .models import TattooImage, Artist

def home(request):
    return render(request, 'core/home.html')

def booking_request(request):
    if request.method == 'POST':
        form = BookingRequestForm(request.POST)
        if form.is_valid():
            booking = form.save()
            # Studio Notification Email
            studio_message = (
                f'New Booking Request from {booking.name}\n\n'
                f'Name: {booking.name}\n'
                f'Email: {booking.email}\n'
                f'Phone: {booking.phone}\n'
                f'Service: {booking.get_service_type_display()}\n'
                f'Preferred date: {booking.preferred_date}\n'
                f'Message: {booking.message}\n'
            )
            send_mail(
                subject=f'New Booking Request from {booking.name}',
                message=studio_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.STUDIO_NOTIFICATION_EMAIL],
                fail_silently=False,
            )
            # Customer Confirmation Email
            customer_message = (
                f"Hi {booking.name},\n\n"
                f"Thank you for your booking request at Ink & Iron Studio!\n\n"
                f"We have received the following details:\n\n"
                f"Service: {booking.get_service_type_display()}\n"
                f"Preferred Date: {booking.preferred_date}\n"
                f"Message: {booking.message}\n\n"
                f"We will review your request and contact you shortly to confirm your appointment.\n\n"
                f"Best regards,\n"
                f"Ink & Iron Tattoo & Piercing Studio\n"
            )
            send_mail(
                subject="Thank you for your booking request - Ink & Iron Studio",
                message=customer_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[booking.email],
                fail_silently=False,
            )
            return redirect('booking_success')
    else:
        form = BookingRequestForm()
    return render(request, 'core/booking_form.html', {'form': form})

def booking_success(request):
    return render(request, 'core/booking_success.html')

def tattoo_gallery(request):
    images = TattooImage.objects.all()
    return render(request, 'core/tattoo_gallery.html', {'images': images})

def artist_list(request):
    artists = Artist.objects.all()
    return render(request, 'core/artists.html', {'artists': artists})