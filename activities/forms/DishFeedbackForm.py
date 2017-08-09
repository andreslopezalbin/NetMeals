from django import forms
from datetime import date
from django.utils.translation import ugettext_lazy as _

from activities.models import DishFeedback
from users.models import Guest
from django.contrib.auth.models import User


class DishFeedbackForm(forms.ModelForm):
    score = forms.IntegerField(max_value=5, min_value=0)
    comment = forms.CharField(max_length=140, widget=forms.TextInput(attrs={'onkeyup': 'countChar(this)'}))

    def __init__(self, *args, **kwargs):
        super(DishFeedbackForm, self).__init__(*args, **kwargs)
        self.fields['score'].label = _("Score")
        self.fields['comment'].label = _("Comment")

    class Meta:
        model = DishFeedback
        fields = ['score', 'comment']

    def clean(self):
        cleaned_data = super(DishFeedbackForm, self).clean()
        comment = cleaned_data.get("comment")

        if len(comment) > 140:
            self.add_error('comment', _('Enter a comment with 140 or less characters'))
