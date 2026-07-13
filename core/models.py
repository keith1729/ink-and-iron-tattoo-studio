from django.db import models

# Create your models here.

class BookingRequest(models.Model):
    SERVICE_CHOICES = [
        ('tattoo', 'Tattoo'),
        ('piercing', 'Piercing'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('declined', 'Declined'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    service_type = models.CharField(max_length=10, choices=SERVICE_CHOICES)
    preferred_date = models.DateField()
    message = models.TextField(blank=True, help_text="Placement, size, design idea, etc.")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.get_service_type_display()} ({self.preferred_date})"

    class Meta:
        ordering = ['-created_at']
