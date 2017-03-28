from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from  django.views.generic.list import ListView

from activities.forms.ActivityForm import ActivityForm
from activities.models import Activity
from activities.services import ActivityService
from django.shortcuts import get_object_or_404
from users.decorators.user_decorators import group_required
from datetime import datetime
from core.util.session_constants import *

from users.models import Monitor


@method_decorator(group_required('Monitor'), name='dispatch')
class CreateActivityView(View):

    def get(self, request, activity_id=None):
        is_edit = False
        is_new = False
        title = "New Activity"
        if activity_id:
            activity = get_object_or_404(Activity, id=activity_id)
            if(activity.owner_id != request.user.id):
                return HttpResponseForbidden()
            is_edit = True
            title = "Edit an Activity"
        else:
            activity = Activity(owner=Monitor(request.user))
            is_new = True
        form = ActivityForm(instance=activity)
        context = {
            'title': title,
            'form': form,
            'is_edit': is_edit,
            'is_new': is_new
        }
        return render(request, 'activities/view_edit.html', context)

    def post(self, request, activity_id=None):
        form = ActivityForm(request.POST)
        success_msg = ''
        error_msg = ''
        if form.is_valid():
            activity = form.create(request)
            if(activity.id is None or activity.id == ''):
                ActivityService.save(activity)
                success_msg = 'Activity saved successfully'
            else:
                ActivityService.update(activity)
                success_msg = 'Activity updated successfully'
        else:
            error_msg = 'There was an error validating form'

        context = {
            'form': form,
            'success_msg': success_msg,
            'error_msg': error_msg

        }
        return render(request, 'activities/view_edit.html', context)

@method_decorator(group_required('Monitor'), name='dispatch')
class ListActivityView(ListView):
    model = Activity
    template_name = 'activities/list.html'
    context_object_name = 'activities'

    def get_context_data(self, **kwargs):
        context = super(ListActivityView, self).get_context_data(**kwargs)
        if(self.request.session.get(SESSION_SUBSCRIPTION_SUCCEEDED)):
            context[SESSION_SUBSCRIPTION_SUCCEEDED] = self.request.session.get(SESSION_SUBSCRIPTION_SUCCEEDED)
            self.request.session[SESSION_SUBSCRIPTION_SUCCEEDED] = None
            context['success_msg'] = 'Successfully subscribed!'
        if (self.request.session.get(SESSION_UNSUBSCRIPTION_SUCCEEDED)):
            context[SESSION_UNSUBSCRIPTION_SUCCEEDED] = self.request.session.get(SESSION_UNSUBSCRIPTION_SUCCEEDED)
            self.request.session[SESSION_UNSUBSCRIPTION_SUCCEEDED] = None
            context['success_msg'] = 'Successfully unsubscribed!'
        return context

    def get_queryset(self):
        self.owner = User.objects.get(id=self.request.user.id)
        return Activity.objects.filter(owner=self.owner)
