from datetime import date

from django import forms
from activities.models import Activity, Dish
from users.models import Chef
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from django.utils.translation import ugettext_lazy as _


class DishForm(forms.ModelForm):
    name = forms.CharField(label=_('Name'))
    description = forms.Textarea()
    photo = forms.CharField(required=False, label=_('Photo'))

    DATEPICKER = {
        'type': 'text',
        'class': 'form-control',
        'id': 'datetimepicker1'
    }
    # Call attrs with form widget
    date = forms.DateTimeField(input_formats=['%d/%m/%Y %h:%m'], widget=forms.DateInput(attrs=DATEPICKER))

    helper = FormHelper()
    helper.form_tag = False
    helper.layout = Layout(
        Field('name', css_class='form-control form-control-success', placeholder='Name'),
        Field('description', css_class='form-control form-control-success', placeholder='Description'),
        Field('photo', css_class='form-control form-control-success', placeholder='Photo')
    )

    class Meta:
        model = Dish
        fields = ['name', 'description', 'photo', 'date']

    def create(self, request):
        owner_id = request.user.id
        owner = Chef.objects.get(guest_ptr_id=owner_id)
        result = Dish(name=self.cleaned_data['name'],
                      description=self.cleaned_data['description'],
                      photo=self.cleaned_data['photo'], date='date',
                      owner=owner,
                      )

        return result
