from django import forms

from activities.models import Activity
from netmeals import settings
from users.models import Monitor
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field

class ActivityForm(forms.ModelForm):
    id = forms.CharField(required=False)
    name = forms.CharField()
    description = forms.Textarea()
    place = forms.CharField()
    latitude = forms.DecimalField(max_digits=23, decimal_places=20)
    longitude = forms.DecimalField(max_digits=23, decimal_places=20)
    start_date = forms.DateField(input_formats=['%d/%m/%Y'])
    start_date.widget.format = '%d/%m/%Y'
    end_date = forms.DateField(input_formats=['%d/%m/%Y'])
    end_date.widget.format = '%d/%m/%Y'

    helper = FormHelper()
    helper.form_tag = False
    helper.field_template="templates/bootstrap3/field.html",
    helper.layout = Layout(
        Field('id', css_class='form-control signup-firstname form-control-success', placeholder='Id', type="hidden"),
        Field('name', css_class='form-control signup-firstname form-control-success', placeholder='Name'),
        Field('description', css_class='form-control signup-surname form-control-success', placeholder='Description'),
        Field('start_date', css_class='form-control signup-surname form-control-success', placeholder='Start date'),
        Field('end_date', css_class='form-control signup-surname form-control-success', placeholder='End date'),
        Field('place', css_class='form-control signup-email form-control-success', placeholder='Place'),
        Field('latitude', css_class='form-control signup-username form-control-success', placeholder='Latitude', type="hidden"),
        Field('longitude', css_class='form-control signup-password form-control-success', placeholder='Longitude', type="hidden"),
    )
    class Meta:
        model = Activity
        fields = ['id', 'name', 'description', 'start_date', 'end_date', 'place', 'latitude', 'longitude']

    def setFieldsDisabledProperty(self, disabled):
        self.fields['id'].disabled = disabled
        self.fields['name'].disabled = disabled
        self.fields['description'].disabled = disabled
        self.fields['start_date'].disabled = disabled
        self.fields['end_date'].disabled = disabled
        self.fields['place'].disabled = disabled
        self.fields['latitude'].disabled = disabled
        self.fields['longitude'].disabled = disabled

        return self

    def create(self, request):
        owner_id = request.user.id
        owner = Monitor.objects.get(guest_ptr_id=owner_id)
        id = self.cleaned_data['id']
        if id == '':
            id = None
        result = Activity(name=self.cleaned_data['name'],
                    description=self.cleaned_data['description'],
                    start_date=self.cleaned_data['start_date'],
                    end_date=self.cleaned_data['end_date'],
                    place=self.cleaned_data['place'],
                    latitude=self.cleaned_data['latitude'],
                    longitude=self.cleaned_data['longitude'],
                    owner=owner,
                    owner_id = owner_id,
                    id = id
                    )

        return result