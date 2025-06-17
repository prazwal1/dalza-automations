from django import forms
from django.forms import inlineformset_factory
from .models import (
    Client, InternetDetails, InsuranceDetails,
    TrackingDetails, UploadedDocument
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
        fields = '__all__'
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


UploadedDocumentFormSet = inlineformset_factory(
    Client,
    UploadedDocument,
    fields=['doc_type', 'file'],
    extra=1,
    can_delete=True
)
