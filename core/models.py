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


class TattooImage(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='tattoos/')
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-uploaded_at']


class Artist(models.Model):
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=150, blank=True, help_text="e.g. Traditional & Neo-traditional")
    bio = models.TextField()
    photo = models.ImageField(upload_to='artists/', blank=True, null=True)
    instagram_handle = models.CharField(max_length=50, blank=True, help_text="Without the @ symbol")
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers appear first")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order', 'name']

