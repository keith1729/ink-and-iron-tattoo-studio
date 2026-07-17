from django.shortcuts import render, redirect
from django.contrib import messages
from django import forms
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .forms import BookingRequestForm
from .models import TattooImage, Artist, PiercingImage

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

def piercing_gallery(request):
    images = PiercingImage.objects.all()
    return render(request, 'core/piercing_gallery.html', {'images': images})


class ConsultationForm(forms.Form):
    name = forms.CharField(max_length=120, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=30, required=False)
    preferred_artist = forms.ChoiceField(required=False)
    preferred_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    notes = forms.CharField(widget=forms.Textarea, required=False)

def _generate_timeslots(days=7):
    # Replace with real availability logic; this is a simple example
    today = timezone.localdate()
    slots = []
    for d in range(days):
        date = today + timezone.timedelta(days=d)
        slots.append({
            'date': date,
            'times': ['10:00', '12:00', '14:00', '16:00'],
        })
    return slots

def consultation(request):
    # Prefill artist choices from DB
    artists = list(Artist.objects.all().order_by('order').values('id', 'name', 'specialty'))
    artist_choices = [('', 'Any artist')] + [(str(a['id']), a['name']) for a in artists]

    if request.method == 'POST':
        form = ConsultationForm(request.POST)
        form.fields['preferred_artist'].choices = artist_choices
        if form.is_valid():
            # TODO: save to DB, send email, or create booking request
            messages.success(request, "Thanks — your consultation request has been received. We'll be in touch.")
            return redirect('consultation')  # or redirect to a thank-you page
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        initial = {}
        if request.user.is_authenticated:
            initial['name'] = request.user.get_full_name() or request.user.username
            initial['email'] = request.user.email
        form = ConsultationForm(initial=initial)
        form.fields['preferred_artist'].choices = artist_choices

    context = {
        'title': 'Consultations - Ink & Iron',
        'meta_description': 'Book a free consultation with our tattoo and piercing artists.',
        'services': [
            {'id': 'tattoo', 'label': 'Tattoo consultation', 'summary': 'Discuss custom pieces and flash'},
            {'id': 'piercing', 'label': 'Piercing consultation', 'summary': 'Ear, facial, and body piercing advice'},
        ],
        'artists': artists,
        'timeslots': _generate_timeslots(10),
        'form': form,
        'location': {
            'address': '123 Main St, Killarney, Co Kerry',
            'map_embed': '',
            'hours': 'Tue–Sat 10:00–18:00'
        },
        'pricing_note': 'Consultations are free; deposits may be required for bookings.',
    }
    return render(request, 'core/consultation.html', context)
