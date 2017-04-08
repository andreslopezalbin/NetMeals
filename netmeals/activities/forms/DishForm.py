from django import forms
from activities.models import Activity, Dish
from users.models import Chef
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field


class DishForm(forms.ModelForm):
    name = forms.CharField()
    description = forms.Textarea()
    photo = forms.CharField(required=False)

    helper = FormHelper()
    helper.form_tag = False
    helper.layout = Layout(
        Field('name', css_class='form-control signup-firstname form-control-success', placeholder='Name'),
        Field('description', css_class='form-control signup-surname form-control-success', placeholder='Description'),
        Field('photo', css_class='form-control signup-email form-control-success', placeholder='Photo')
    )

    class Meta:
        model = Dish
        fields = ['name', 'description', 'photo']

    def create(self, request):
        owner_id = request.user.id
        owner = Chef.objects.get(guest_ptr_id=owner_id)
        result = Dish(name=self.cleaned_data['name'],
                      description=self.cleaned_data['description'],
                      photo=self.cleaned_data['photo'],
                      owner=owner,
                      )

        return result
