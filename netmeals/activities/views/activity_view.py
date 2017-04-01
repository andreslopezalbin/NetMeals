import datetime
from urlparse import urlparse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, request
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView
from django.views.generic import FormView
from  django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import resolve, reverse

from activities.forms.ActivityForm import ActivityForm
from activities.models import Activity
from users.models import Guest
from core.util.session_constants import *

class ActivityDetailView(View):

    def get(self, request, activity_id):
        activity = get_object_or_404(Activity, id=activity_id)
        form = ActivityForm(instance=activity)
        form.setFieldsDisabledProperty(True)
        context = {
            'title': "Detail of an Activity",
            'form': form,
            'is_edit': False
        }

        if (request.session.get(SESSION_SUBSCRIPTION_SUCCEEDED)):
            context[SESSION_SUBSCRIPTION_SUCCEEDED] = request.session.get(SESSION_SUBSCRIPTION_SUCCEEDED)
            request.session[SESSION_SUBSCRIPTION_SUCCEEDED] = None
            context['success_msg'] = 'Successfully subscribed!'
        if (request.session.get(SESSION_UNSUBSCRIPTION_SUCCEEDED)):
            context[SESSION_UNSUBSCRIPTION_SUCCEEDED] = request.session.get(SESSION_UNSUBSCRIPTION_SUCCEEDED)
            request.session[SESSION_UNSUBSCRIPTION_SUCCEEDED] = None
            context['success_msg'] = 'Successfully unsubscribed!'

        return render(request, 'activities/view_edit.html', context)

class ActivitySubscriptionView(View):

    def get(self, request, activity_id):
        activity = get_object_or_404(Activity, id=activity_id)

        guest = Guest.objects.get(id=request.user.id)

        if(activity.owner_id != request.user.id):
            activity.assistants.add(guest)

        result_url = "/"
        if(request.META.get('HTTP_REFERER') is not None):
            result_url =  urlparse(request.META.get('HTTP_REFERER')).path
            request.session[SESSION_SUBSCRIPTION_SUCCEEDED] = True

        return HttpResponseRedirect(result_url)


class ActivityUnsubscriptionView(View):

    def get(self, request, activity_id):
        activity = get_object_or_404(Activity, id=activity_id)

        guest = Guest.objects.get(id=request.user.id)
        activity.assistants.remove(guest)

        result_url = "/"
        if(request.META.get('HTTP_REFERER') is not None):
            result_url =  urlparse(request.META.get('HTTP_REFERER')).path
            request.session[SESSION_UNSUBSCRIPTION_SUCCEEDED] = True

        return HttpResponseRedirect(result_url)

class ListSubscribedActivitiesView(ListView):
    model = Activity
    template_name = 'activities/list.html'
    context_object_name = 'activities'

    def get_context_data(self, **kwargs):
        context = super(ListSubscribedActivitiesView, self).get_context_data(**kwargs)
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
        today = datetime.datetime.today().date()
        return Guest.objects.get(id=self.request.user.id).activity_assisted.filter(end_date__gte=today, start_date__lte=today)

class ListAllActivityView(ListView):
    model = Activity
    template_name = 'activities/list.html'
    context_object_name = 'activities'

    def get_context_data(self, **kwargs):
        context = super(ListAllActivityView, self).get_context_data(**kwargs)
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
        today = datetime.datetime.today().date()
        return Activity.objects.filter(end_date__gte=today, start_date__lte=today)
