from django import forms
from .models import ProfileUser, CustomUser
from django.core.exceptions import ValidationError

class CustomUserForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name','email', 'password','confirm_password']
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
            'password': 'Password',
            'confirm_password': 'Confirm Password'
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('Passwords do not match')

        return cleaned_data

def validate_positive_number(value):
    if not value.isdigit() or int(value) <= 0:
        raise ValidationError('Phone number must be a positive number.')

class ProfileUserForm(forms.ModelForm):
    phone_number = forms.CharField(
        validators=[validate_positive_number],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'})
    )

    class Meta:
        model = ProfileUser
        fields = ['phone_number', 'gender', 'date_of_birth', 'role']
        labels = {
            'phone_number': 'Phone Number',
            'gender': 'Gender',
            'date_of_birth': 'Date of Birth',
            'role': 'Role'
        }
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD', 'type': 'date'}),
            'role': forms.Select(attrs={'class': 'form-control'})
        }



