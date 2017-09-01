from datetime import date

from django import forms
from activities.models import Dish
from users.models import Chef
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from django.utils.translation import ugettext_lazy as _


class DishForm(forms.ModelForm):
    name = forms.CharField(label=_('Name'))
    description = forms.CharField(widget=forms.Textarea, label=_('Description'))
    short_description = forms.CharField(widget=forms.Textarea, max_length=140, label=_('Shot description'))
    photo = forms.CharField(required=False, label=_('Photo'))
    date = forms.DateField(required=True, input_formats=['%d/%m/%Y'])
    date.widget.format = '%d/%m/%Y'
    date.widget.attrs['readonly'] = True
    hour = forms.TimeField(required=True)
    hour.widget.attrs['readonly'] = True
    max_assistants = forms.IntegerField()
    place = forms.CharField(max_length=250)
    contribution = forms.DecimalField()
    latitude = forms.DecimalField(max_digits=23, decimal_places=20)
    longitude = forms.DecimalField(max_digits=23, decimal_places=20)

    def __init__(self, *args, **kwargs):
        place = kwargs.pop('place', None)
        super(DishForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = _("Name")
        self.fields['description'].label = _("Description")
        self.fields['short_description'].label = _("Short description")
        self.fields['photo'].label = _("Photo")
        self.fields['date'].label = _("Date")
        self.fields['date'].widget.attrs['class'] = 'dateinput'
        self.fields['hour'].label = _("Hour")
        self.fields['hour'].widget.attrs['class'] = 'timeinput'
        self.fields['max_assistants'].label = _("Max assistants")
        self.fields['contribution'].label = _('contribution')
        self.fields['place'].label = _('Place')
        self.fields['place'].widget.attrs['id'] = 'id_place'
        self.fields['longitude'].widget = forms.HiddenInput()
        self.fields['longitude'].widget.attrs['id'] = 'id_longitude'
        self.fields['latitude'].widget = forms.HiddenInput()
        self.fields['latitude'].widget.attrs['id'] = 'id_latitude'
        if place:
            self.fields['place'].initial = place

    class Meta:
        model = Dish
        fields = ['name', 'description', 'short_description', 'photo', 'date', 'hour', 'max_assistants', 'contribution',
                  'place', 'longitude', 'latitude',
                  ]

    def clean(self):
        if self.cleaned_data['max_assistants'] <= 0:
            self.add_error('max_assistants', _("You must add more assistants"))
        if self.cleaned_data['contribution'] <= 0:
            self.add_error('contribution', _("WOW! Its so cheap!"))
        if self.cleaned_data.get('date') < date.today():
            self.add_error('date', _("You cant share a old dish, sorry"))
        return self.cleaned_data

    def create(self, request):
        owner_id = request.user.id
        owner = Chef.objects.get(guest_ptr_id=owner_id)
        result = Dish(name=self.cleaned_data['name'],
                      description=self.cleaned_data['description'],
                      short_description=self.cleaned_data['short_description'],
                      photo=self.cleaned_data['photo'],
                      date=self.cleaned_data['date'],
                      hour=self.cleaned_data['hour'],
                      owner=owner,
                      max_assistants=self.cleaned_data['max_assistants'],
                      contribution=self.cleaned_data['contribution'],
                      place=self.cleaned_data['place'],
                      latitude=self.cleaned_data['latitude'],
                      longitude=self.cleaned_data['longitude'],
                      )

        return result
