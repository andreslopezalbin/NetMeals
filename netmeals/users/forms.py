from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.core.validators import validate_email


class LoginForm(forms.Form):
    username = forms.CharField(label="username", required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Your email'}))
    password = forms.CharField(label="Password", max_length=32,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Your password'}),
                               required=True)

    def clean_email(self):
        username = self.cleaned_data.get('username')
        return username

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            try:
                user = authenticate(username=username, password=password)
                if not user:
                    raise forms.ValidationError(_("Sorry, that login was invalid. Please try again."))
            except:
                raise forms.ValidationError(_("Sorry, that login was invalid. Please try again."))

        return self.cleaned_data
