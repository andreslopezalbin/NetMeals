from django import forms
from activities.models import Activity, Monitor
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field

class ActivityForm(forms.ModelForm):
    name = forms.CharField()
    description = forms.Textarea()
    place = forms.CharField()
    # latitude = forms.DecimalField(max_digits=9, decimal_places=6)
    # longitude = forms.DecimalField(max_digits=9, decimal_places=6)


    helper = FormHelper()
    helper.form_tag = False
    helper.layout = Layout(
        Field('name', css_class='form-control signup-firstname form-control-success', placeholder='Name'),
        Field('description', css_class='form-control signup-surname form-control-success', placeholder='Description'),
        Field('place', css_class='form-control signup-email form-control-success', placeholder='Place'),
        # Field('latitude', css_class='form-control signup-username form-control-success', placeholder='Username'),
        # Field('longitude', css_class='form-control signup-password form-control-success', placeholder='Password', id='signup-userPassword'),
    )

    class Meta:
        model = Activity
        fields = ['name', 'description', 'place']

    def create(self, request):
        owner_id = request.user.id
        owner = Monitor.objects.get(guest_ptr_id=owner_id)
        result = Activity(name=self.cleaned_data['name'],
                    description=self.cleaned_data['description'],
                    place=self.cleaned_data['place'],
                    latitude=0,
                    longitude=0,
                    owner=owner,
                    owner_id = owner_id
                    )

        return result