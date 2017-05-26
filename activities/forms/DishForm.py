from datetime import date

from django import forms
from django.core.exceptions import ValidationError
from django.db.models.fields import IntegerField

from activities.models import Dish
from users.models import Chef
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from django.utils.translation import ugettext_lazy as _


class DishForm(forms.ModelForm):
    name = forms.CharField(label=_('Name'))
    description = forms.CharField(widget=forms.Textarea, label=_('Description'))
    photo = forms.CharField(required=False, label=_('Photo'))
    date = forms.DateField(required=True)
    date.widget.attrs['readonly'] = True
    hour = forms.TimeField(required=True)
    hour.widget.attrs['readonly'] = True
    max_assistants = forms.IntegerField()
    contribution = forms.DecimalField()

    helper = FormHelper()
    helper.form_tag = False
    helper.layout = Layout(
        Field('name', css_class='form-control form-control-success', placeholder=_('Name')),
        Field('description', css_class='form-control form-control-success', placeholder=_('Description')),
        Field('photo', css_class='form-control form-control-success', placeholder=_('Photo')),
        Field('date', css_class='form-control form-control-success', placeholder=_('date')),
        Field('hour', css_class='form-control form-control-success', placeholder=_('hour')),
        Field('max_assistants', css_class='form-control form-control-success', placeholder=_('max_assistants')),
        Field('contribution', css_class='form-control form-control-success', placeholder=_('contribution')),

    )

    class Meta:
        model = Dish
        fields = ['name', 'description', 'photo', 'date', 'hour', 'max_assistants', 'contribution']

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
                      photo=self.cleaned_data['photo'],
                      date=self.cleaned_data['date'],
                      hour=self.cleaned_data['hour'],
                      owner=owner,
                      max_assistants=self.cleaned_data['max_assistants'],
                      contribution=self.cleaned_data['contribution']
                      )

        return result
