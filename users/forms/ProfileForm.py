from django import forms
from datetime import date
from django.utils.translation import ugettext_lazy as _

from users.models import Guest
from django.contrib.auth.models import User


class GuestForm(forms.ModelForm):
    username = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    phone = forms.RegexField(regex=r'^\+?1?\d{9,15}$',
                             error_message=_("Must be in 999999999 format"))
    birth_date = forms.DateField(required=False, input_formats=['%d/%m/%Y'])

    def __init__(self, *args, **kwargs):
        super(GuestForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = _("Username")
        self.fields['first_name'].label = _("Name")
        self.fields['last_name'].label = _("Surname")
        self.fields['email'].label = _("Email")
        self.fields['phone'].label = _("Phone")
        self.fields['birth_date'].label = _("Birthday")
        self.fields['birth_date'].widget.attrs['class'] = 'dateinput'
        self.fields['birth_date'].widget.attrs['readonly'] = True

    class Meta:
        model = Guest
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'birth_date']

    def clean(self):
        cleaned_data = super(GuestForm, self).clean()
        birth_date = cleaned_data.get("birth_date")
        email = cleaned_data.get("email")

        if birth_date is not None and birth_date > date.today():
            self.add_error('birth_date', _('You must enter a valid date'))
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            self.add_error('email', _('Email is already in use'))
