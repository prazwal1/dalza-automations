from django import forms
from .models import CustomUser

class CustomUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'phone_number', 'role', 'is_active', 'password']

    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Editing existing user: password is optional
            self.fields['password'].required = False
        else:
            # Creating new user: password is required
            self.fields['password'].required = True

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if self.instance and self.instance.pk:
            # Editing: if password not provided, keep existing
            if not password:
                return self.instance.password
        else:
            # Creating: password must be provided (handled by required=True)
            if not password:
                raise forms.ValidationError("Password is required.")
        return password

    def save(self, commit=True):
        user = super(CustomUserForm, self).save(commit=False)
        password = self.cleaned_data.get('password')
        if password and (not self.instance.pk or password != self.instance.password):
            user.set_password(password)
        if commit:
            user.save()
        return user