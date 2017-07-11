from symbol import decorators

import datetime
from crispy_forms.bootstrap import AppendedText
from django import forms
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage

from activities.models import Activity
from netmeals import settings
from users.models import Monitor
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML


class ActivityForm(forms.ModelForm):
    id = forms.CharField(required=False)
    is_periodically = forms.CharField(required=False)
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

    start_hour = forms.TimeField()
    start_hour.widget.attrs['readonly'] = True
    end_hour = forms.TimeField()
    end_hour.widget.attrs['readonly'] = True

    price_per_person = forms.DecimalField(max_digits=5, decimal_places=2)

    type_of_activity = forms.ChoiceField(
        choices=(
            ('one_time', " This is a one time activity"),
            ('periodically', " This is a periodically activity")
        ),
        widget=forms.RadioSelect,
        initial="one_time"
    )

    helper = FormHelper()
    helper.form_tag = False
    helper.layout = Layout(
        Field('id', type="hidden"),
        Field('is_periodically', type="hidden"),
        Field('photo', css_class='form-control activity-photo form-control-success', placeholder='Photo', accept="image/x-png,image/gif,image/jpeg"),
        Field('name', css_class='form-control activity-name form-control-success', placeholder='Name'),
        Field('short_description', css_class='form-control activity-short-description form-control-success', placeholder='Short description'),
        Field('description', css_class='form-control activity-description form-control-success', placeholder='Description'),
        Field('price_per_person', css_class='form-control activity-price form-control-success', placeholder='Price' ,max='999'),
        Field('type_of_activity', css_class="activity-type"),
        AppendedText('start_date', '<i class="fa fa-calendar activity-date" aria-hidden="true"></i>', active=True, css_class='form-control activity-date form-control-success', placeholder='Start date'),
        AppendedText('start_hour', '<i class="fa fa-clock-o activity-time" aria-hidden="true"></i>', active=True, css_class='form-control activity-date form-control-success', placeholder='Start hour'),
        AppendedText('end_hour', '<i class="fa fa-clock-o activity-time" aria-hidden="true"></i>', active=True, css_class='form-control activity-date form-control-success', placeholder='End hour'),
        Field('place', css_class='form-control activity-place form-control-success', placeholder='Place'),
        Field('latitude', type="hidden"),
        Field('longitude', type="hidden"),
    )
    class Meta:
        model = Activity
        fields = ['id', 'is_periodically', 'photo', 'name', 'short_description', 'description', 'price_per_person', 'start_date', 'start_hour', 'end_hour', 'place', 'latitude', 'longitude']

    def clean(self):
        form_data = self.cleaned_data
        is_periodically = form_data['is_periodically']

        if is_periodically == "true":
            errors = self._errors
            del errors['start_date']
            del errors['start_hour']
            del errors['end_hour']

            form_data['start_date'] = datetime.datetime.now()

        return form_data

    def setFieldsDisabledProperty(self, disabled):
        self.fields['id'].disabled = disabled
        self.fields['photo'].disabled = disabled
        self.fields['name'].disabled = disabled
        self.fields['short_description'].disabled = disabled
        self.fields['description'].disabled = disabled
        if(disabled):
            self.fields['type_of_activity'].widget.attrs = {'disabled':'disabled'}
        self.fields['price_per_person'].disabled = disabled
        self.fields['type_of_activity'].widget.disabled = disabled
        self.fields['start_date'].disabled = disabled
        self.fields['start_hour'].disabled = disabled
        self.fields['end_hour'].disabled = disabled
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

        end_date = datetime.datetime.now()
        if 'end_date' in self.cleaned_data:
            end_date = self.cleaned_data['end_date']

        result = Activity(name=self.cleaned_data['name'],
                    short_description=self.cleaned_data['short_description'],
                    description=self.cleaned_data['description'],
                    place=self.cleaned_data['place'],
                    start_date=self.cleaned_data['start_date'],
                    end_date=end_date,
                    price_per_person=self.cleaned_data['price_per_person'],
                    latitude=self.cleaned_data['latitude'],
                    longitude=self.cleaned_data['longitude'],
                    owner=owner,
                    owner_id = owner_id,
                    id = id
                    )

        if uploaded_photo_url != '':
            result.photo = uploaded_photo_url

        return result