from django.db import models
from user_authen.models import CustomUser

REGION_CHOICES = [
        ('Everest Region', 'Everest Region'),
        ('Annapurna Circuit', 'Annapurna Region'),
        ('Langtang Valley', 'Langtang Valley'),
        ('Manaslu Circuit', 'Manaslu Circuit')
        # Add more regions as needed
    ]

class TravelBooking(models.Model):
    # Basic Info
    nationality = models.CharField(max_length=100, blank=True)
    travel_from = models.CharField(max_length=100, blank=True)

    package_id = models.CharField(max_length=50, choices=REGION_CHOICES, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    
    # Personal Details
    surname = models.CharField(max_length=100, blank=True)
    given_name = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    dob = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    
    # Emergency & Passport
    emergency_contact = models.CharField(max_length=100, blank=True)
    passport_no = models.CharField(max_length=50, blank=True)
    passport_image_path = models.CharField(max_length=255, blank=True, null=True)
    profile_image_path = models.CharField(max_length=255, blank=True, null=True)

    # Meta
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='travel_bookings')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Additional Fields
    is_active = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.given_name} {self.surname} - {self.package_id}"