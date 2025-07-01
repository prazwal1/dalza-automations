from django import forms
from django.forms import inlineformset_factory
from .models import (
    Client, InternetDetails, InsuranceDetails, ServicePlan,
    TrackingDetails, UploadedDocument, Address, UserGroup
)
from insurance.permissions import get_allowed_fields_by_role


class ClientForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            allowed_fields = get_allowed_fields_by_role(user.role)
            if allowed_fields != '__all__':
                allowed = set(allowed_fields)
                for field_name in list(self.fields):
                    if field_name not in allowed:
                        self.fields.pop(field_name)

    class Meta:
        model = Client
        exclude = ('agent', 'created_by', 'unique_id', 'perma_address','address')
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }


class InternetDetailsForm(forms.ModelForm):
    class Meta:
        model = InternetDetails
        exclude = ('customer',)
        widgets = {
            'account_expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'user_group' in self.fields:
            choices = self.fields['user_group'].queryset
            if choices.exists():
                self.fields['user_group'].initial = choices.first().pk  # Select first option

        if 'service_plan' in self.fields:
            choices = self.fields['service_plan'].queryset
            if choices.exists():
                self.fields['service_plan'].initial = choices.first().pk
        
        if 'payment_status' in self.fields:
            self.fields['payment_status'].choices = [
                ('paid', 'Paid'),
                ('unpaid', 'Unpaid'),
                ('partial', 'Partial')
            ]
            self.fields['payment_status'].initial = 'unpaid'

class InsuranceDetailsForm(forms.ModelForm):
    class Meta:
        model = InsuranceDetails
        exclude = ('customer',)


class TrackingDetailsForm(forms.ModelForm):
    class Meta:
        model = TrackingDetails
        exclude = ('customer',)
        widgets = {
            'travel_start_date': forms.DateInput(attrs={'type': 'date'}),
            'travel_end_date': forms.DateInput(attrs={'type': 'date'}),
        }


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['city', 'province', 'district', 'ward_no', 'street_name', 'country', 'zip']

UploadedDocumentFormSet = inlineformset_factory(
    Client,
    UploadedDocument,
    fields=['doc_type', 'file'],
    extra=1,
    can_delete=True
)


class UserGroupForm(forms.ModelForm):
    class Meta:
        model = UserGroup
        fields = ['name', 'description']

class ServicePlanForm(forms.ModelForm):
    class Meta:
        model = ServicePlan
        fields = ['name', 'description']
        
        
class ClientFilterForm(forms.Form):
    # Main client fields
    first_name = forms.CharField(required=False, label="First Name")
    last_name = forms.CharField(required=False, label="Last Name")
    email = forms.CharField(required=False, label="Email")
    phone_number = forms.CharField(required=False, label="Phone Number")
    vat_pan = forms.CharField(required=False, label="VAT/PAN")
    company_name = forms.CharField(required=False, label="Company Name")
    # Address fields
    city = forms.CharField(required=False, label="City")
    province = forms.CharField(required=False, label="Province")
    # InternetDetails fields
    username_or_mac = forms.CharField(required=False, label="Username or MAC")
    service_plan = forms.ModelChoiceField(queryset=ServicePlan.objects.all(), required=False, label="Service Plan")
    user_group = forms.ModelChoiceField(queryset=UserGroup.objects.all(), required=False, label="User Group")
    # InsuranceDetails fields
    insurance_comments = forms.CharField(required=False, label="Insurance Comments")
    # TrackingDetails fields
    travel_from = forms.CharField(required=False, label="Travel From")
    package = forms.CharField(required=False, label="Package")
    # General search
    search = forms.CharField(required=False, label="General Search")