from django import forms
from .models import TravelBooking
from .permissions import get_allowed_fields_by_role  # Adjust the import path as needed

class TravelBookingForm(forms.ModelForm):
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
        model = TravelBooking
        fields = '__all__'
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
        help_texts = {
            'passport_image_path': 'Upload a clear image of your passport.',
            'profile_image_path': 'Upload a clear profile picture.',
        }   