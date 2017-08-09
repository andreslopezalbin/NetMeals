import datetime
from urllib.parse import urlparse

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from  django.views.generic.list import ListView
from django.shortcuts import get_object_or_404

from activities.forms.ActivityForm import ActivityForm
from activities.models import Activity
from activities.services import activity_service
from core.util import session_utils
from users.models import Guest

class ActivityDetailView(View):

    def get(self, request, activity_id):
        activity = get_object_or_404(Activity, id=activity_id)
        form = ActivityForm(instance=activity)
        form.setFieldsDisabledProperty(True)
        activity_photo = activity.photo
        context = {
            'title': "Detail of an Activity",
            'form': form,
            'is_edit': False,
            'activity_id': activity.id,
            'activity_photo': activity_photo,
            'activity': activity
        }

        session_utils.set_context_with_activity_session(self.request.session, context)

        return render(request, 'activities/view_edit.html', context)

class ActivitySubscriptionView(View):

    def post(self, request, activity_id):
        activity_service.subscribe(activity_id, request)
        result_url = "/"
        if (request.META.get('HTTP_REFERER') is not None):
            result_url = urlparse(request.META.get('HTTP_REFERER')).path

        return HttpResponseRedirect(result_url)

class ActivityUnsubscriptionView(View):

    def post(self, request, activity_id):
        activity_service.unsubscribe(activity_id, request)
        result_url = "/"
        if(request.META.get('HTTP_REFERER') is not None):
            result_url = urlparse(request.META.get('HTTP_REFERER')).path

        return HttpResponseRedirect(result_url)

class ListSubscribedActivitiesView(ListView):
    model = Activity
    template_name = 'activities/list.html'
    context_object_name = 'activities'

    def get_context_data(self, **kwargs):
        context = super(ListSubscribedActivitiesView, self).get_context_data(**kwargs)

        session_utils.set_context_with_activity_session(self.request.session, context)

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

        if(not context['activities']):
            context['activities'] = []

        session_utils.set_context_with_activity_session(self.request.session, context)

        return context

    def get_queryset(self):
        today = datetime.datetime.today().date()
        return Activity.objects.filter(end_date__gte=today, start_date__lte=today)
