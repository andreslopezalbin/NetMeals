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
    phone = forms.RegexField(regex=r'^\d{9}$',
                             error_message=_("Must be in 999999999 format"))
    place = forms.CharField(max_length=250, required=False)
    latitude = forms.DecimalField(max_digits=23, decimal_places=20, required=False)
    longitude = forms.DecimalField(max_digits=23, decimal_places=20, required=False)

    def __init__(self, *args, **kwargs):
        super(GuestForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = _("Username")
        self.fields['first_name'].label = _("Name")
        self.fields['last_name'].label = _("Surname")
        self.fields['email'].label = _("Email")
        self.fields['phone'].label = _("Phone")
        self.fields['place'].label = _("Place")
        self.fields['place'].widget.attrs['id'] = 'id_place'
        self.fields['longitude'].widget = forms.HiddenInput()
        self.fields['longitude'].widget.attrs['id'] = 'id_longitude'
        self.fields['latitude'].widget = forms.HiddenInput()
        self.fields['latitude'].widget.attrs['id'] = 'id_latitude'

    class Meta:
        model = Guest
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'place', 'latitude',
                  'longitude']

    def clean(self):
        cleaned_data = super(GuestForm, self).clean()
        email = cleaned_data.get("email")

        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            self.add_error('email', _('Email is already in use'))
        if cleaned_data.get('place') and (cleaned_data.get('longitude') is None or cleaned_data.get('latitude') is None):
            self.add_error('place', _('Something went wrong, please try later'))


class AboutMeForm(forms.ModelForm):
    birth_date = forms.DateField(required=False, input_formats=['%d/%m/%Y'])
    abstract = forms.CharField(max_length=500,
                               widget=forms.Textarea(attrs={'onkeyup': 'countCharAbstract(this)'}))
    speciality = forms.CharField(max_length=140,
                                 widget=forms.Textarea(attrs={'onkeyup': 'countCharSpeciality(this)'}))

    def __init__(self, *args, **kwargs):
        super(AboutMeForm, self).__init__(*args, **kwargs)
        self.fields['birth_date'].label = _("Birthday")
        self.fields['birth_date'].widget.attrs['class'] = 'dateinput'
        self.fields['birth_date'].widget.attrs['readonly'] = True
        self.fields['abstract'].label = _("Abstract")
        self.fields['abstract'].widget.attrs['class'] = 'abstract'
        self.fields['speciality'].label = _("Speciality")
        self.fields['speciality'].widget.attrs['class'] = 'speciality'

    class Meta:
        model = Guest
        fields = ['birth_date', 'abstract', 'speciality']

    def clean(self):
        cleaned_data = super(AboutMeForm, self).clean()
        birth_date = cleaned_data.get("birth_date")

        if birth_date is not None and birth_date > date.today():
            self.add_error('birth_date', _('You must enter a valid date'))
