from django import forms
from activities.models import Guest
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field

# from django.contrib.auth.models import User
# from django.core.exceptions import ValidationError


class GuestRegistrationForm(forms.ModelForm):
    first_name = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Guest
        fields = ['email', 'first_name', 'password']


class SignUpForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    repeated_password = forms.CharField(widget=forms.PasswordInput)



    helper = FormHelper()
    helper.form_tag = False
    helper.layout = Layout(
        Field('first_name', css_class='form-control signup-firstname form-control-success', placeholder='First Name'),
        Field('last_name', css_class='form-control signup-surname form-control-success', placeholder='Last Name'),
        Field('email', css_class='form-control signup-email form-control-success', placeholder='Email'),
        Field('username', css_class='form-control signup-username form-control-success', placeholder='Username'),
        Field('password', css_class='form-control signup-password form-control-success', placeholder='Password', id='signup-userPassword'),
        Field('repeated_password', css_class='form-control signup-password-repeat form-control-success', placeholder='Repeat Password', id = 'signup-userPassword-repeat'),
        Div(css_class='repeatPassword-error form-control-feedback', id='matchPasswordErrorMessage')
    )

    class Meta:
        model = Guest
        fields = ['first_name', 'last_name', 'email', 'username',  'password']