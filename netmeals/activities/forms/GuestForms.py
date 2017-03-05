from django import forms
from activities.models import Guest


# from django.contrib.auth.models import User
# from django.core.exceptions import ValidationError


class GuestRegistrationForm(forms.ModelForm):
    first_name = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Guest
        fields = ['email', 'first_name', 'password']
