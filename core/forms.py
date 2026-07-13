from django import forms
from .models import BookingRequest

class BookingRequestForm(forms.ModelForm):
    class Meta:
        model = BookingRequest
        fields = ['name', 'email', 'phone', 'service_type', 'preferred_date', 'message']
        widgets = {
            'preferred_date': forms.DateInput(attrs={'type': 'date'}),
            'message': forms.Textarea(attrs={'rows': 4}),
        }
