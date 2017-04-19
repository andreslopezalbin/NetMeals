from django import forms
from django.core.files.storage import FileSystemStorage

from activities.models import Activity
from netmeals import settings
from users.models import Monitor
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML


class ActivityForm(forms.ModelForm):
    id = forms.CharField(required=False)
    name = forms.CharField(max_length=70)
    short_description = forms.CharField(widget=forms.Textarea, max_length= 140)
    description = forms.CharField(widget=forms.Textarea)
    place = forms.CharField()
    latitude = forms.DecimalField(max_digits=23, decimal_places=20)
    longitude = forms.DecimalField(max_digits=23, decimal_places=20)
    photo = forms.FileField(required=False)
    start_date = forms.DateField(input_formats=['%d/%m/%Y'])
    start_date.widget.format = '%d/%m/%Y'
    start_date.widget.attrs['readonly'] = True
    end_date = forms.DateField(input_formats=['%d/%m/%Y'])
    end_date.widget.format = '%d/%m/%Y'
    end_date.widget.attrs['readonly'] = True

    helper = FormHelper()
    helper.form_tag = False
    helper.field_template="templates/bootstrap3/field.html",
    helper.layout = Layout(
        Field('id', type="hidden"),
        Field('photo', css_class='form-control activity-photo form-control-success', placeholder='Photo', accept="image/x-png,image/gif,image/jpeg"),
        Field('name', css_class='form-control activity-name form-control-success', placeholder='Name'),
        Field('short_description', css_class='form-control activity-short-description form-control-success', placeholder='Short description'),
        Field('description', css_class='form-control activity-description form-control-success', placeholder='Description'),
        Field('start_date', css_class='form-control activity-date form-control-success', placeholder='Start date'),
        Field('end_date', css_class='form-control activity-date form-control-success', placeholder='End date'),
        Field('place', css_class='form-control activity-place form-control-success', placeholder='Place'),
        Field('latitude', type="hidden"),
        Field('longitude', type="hidden"),
    )
    class Meta:
        model = Activity
        fields = ['id', 'photo', 'name', 'short_description', 'description', 'start_date', 'end_date', 'place', 'latitude', 'longitude']

    def setFieldsDisabledProperty(self, disabled):
        self.fields['id'].disabled = disabled
        self.fields['photo'].disabled = disabled
        self.fields['name'].disabled = disabled
        self.fields['short_description'].disabled = disabled
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
        uploaded_photo_url = ''
        if request.FILES:
            photo = request.FILES['photo']
            fs = FileSystemStorage()
            filename = fs.save(photo.name, photo)
            uploaded_photo_url = fs.url(filename)
        if id == '':
            id = None
        result = Activity(name=self.cleaned_data['name'],
                    short_description=self.cleaned_data['short_description'],
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

        if uploaded_photo_url != '':
            result.photo = uploaded_photo_url

        return result