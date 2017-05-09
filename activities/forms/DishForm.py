from datetime import date

from django import forms
from activities.models import Dish
from users.models import Chef
from django.utils.translation import ugettext_lazy as _


class DishForm(forms.ModelForm):
    name = forms.CharField(label=_('Name'))
    description = forms.Textarea()
    photo = forms.CharField(required=False, label=_('Photo'))
    date = forms.DateInput()

    class Meta:
        model = Dish
        fields = ['name', 'description', 'photo', 'date']

    def create(self, request):
        owner_id = request.user.id
        owner = Chef.objects.get(guest_ptr_id=owner_id)
        result = Dish(name=self.cleaned_data['name'],
                      description=self.cleaned_data['description'],
                      photo=self.cleaned_data['photo'],
                      date=self.cleaned_data['date'],
                      owner=owner,
                      )

        return result
