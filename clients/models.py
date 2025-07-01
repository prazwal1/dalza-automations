# models.py
from django.db import models
from user_authen.models import CustomUser


class ServicePlan(models.Model):
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='service_plans_created')
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name


class UserGroup(models.Model):
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='user_groups_created')
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name

class Address(models.Model):
    zip = models.CharField(max_length=10, null=True, blank=True)
    country = models.CharField(max_length=100, blank=True, default="")
    city = models.CharField(max_length=100, null=True, blank=True)
    province = models.CharField(max_length=100, null=True, blank=True)
    district = models.CharField(max_length=100, null= True, blank=True)
    ward_no = models.CharField(max_length=10, null=True, blank=True)
    street_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.street_name}, Ward {self.ward_no}, {self.district}, {self.city}, {self.province}"


class Client(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20)

    # Current Address Fields
    address = models.OneToOneField(Address, related_name="current_client", on_delete=models.CASCADE)
    perma_address = models.OneToOneField(Address, related_name="permanent_client", on_delete=models.CASCADE, null=True, blank=True)

    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    vat_pan = models.CharField(max_length=50, blank=True)
    nid_citizen = models.CharField(max_length=50, blank=True)
    passport_number = models.CharField(max_length=50, blank=True)
    company_name = models.CharField(max_length=255, blank=True)

    agent = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='clients')
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    unique_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    extra_field_1 = models.CharField(max_length=255, blank=True, null=True)
    extra_field_2 = models.CharField(max_length=255, blank=True, null=True)
    extra_field_3 = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class InternetDetails(models.Model):
    customer = models.OneToOneField(Client, on_delete=models.CASCADE)
    username_or_mac = models.CharField(max_length=100)
    enable = models.BooleanField(default=True)
    mac_user = models.BooleanField(default=False)
    password = models.CharField(max_length=128, blank=True)
    mac_address_of_cm = models.CharField(max_length=100, blank=True)
    simultaneous_use = models.PositiveIntegerField(default=1)
    service_plan = models.ForeignKey(ServicePlan, on_delete=models.SET_NULL, null=True)
    user_group = models.ForeignKey(UserGroup, on_delete=models.SET_NULL, null=True)
    download_limit = models.BigIntegerField(default=0)
    upload_limit = models.BigIntegerField(default=0)
    total_limit = models.BigIntegerField(default=0)
    account_expiry_date = models.DateField(null=True, blank=True)
    radius_comments = models.TextField(blank=True)
    radius_attribute = models.TextField(blank=True)
    marketed_by = models.CharField(max_length=100, blank=True, null=True)
    billed_by = models.CharField(max_length=100, blank=True, null=True)
    payment_status = models.CharField(max_length=20, blank=True, choices=[('paid', 'Paid'), ('unpaid', 'Unpaid'), ('partial', 'Partial')])
    account_owner = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null= True, blank=True, related_name="account_owner")
    extra_field_1 = models.CharField(max_length=255, blank=True, null=True)
    extra_field_2 = models.CharField(max_length=255, blank=True, null=True)

class InsuranceDetails(models.Model):
    customer = models.OneToOneField(Client, on_delete=models.CASCADE)
    insurance_comments = models.TextField(blank=True)


class TrackingDetails(models.Model):
    customer = models.OneToOneField(Client, on_delete=models.CASCADE)
    travel_from = models.CharField(max_length=100)
    emergency_contact = models.CharField(max_length=100)
    package = models.CharField(max_length=100)
    travel_start_date = models.DateField(null=True, blank=True)
    travel_end_date = models.DateField(null=True, blank=True)


class UploadedDocument(models.Model):
    DOCUMENT_TYPES = [
        ('passport', 'Passport'),
        ('kyc', 'KYC'),
        ('citizen', 'Citizen Card'),
        ('photo', 'Photo'),
    ]
    customer = models.ForeignKey(Client, on_delete=models.CASCADE)
    doc_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    file = models.FileField(upload_to='uploads/')
