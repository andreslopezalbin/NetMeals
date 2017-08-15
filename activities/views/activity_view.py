import datetime
from urllib.parse import urlparse

from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from  django.views.generic.list import ListView
from django.shortcuts import get_object_or_404

from activities.forms.ActivityForm import ActivityForm
from activities.models import Activity, ActivityTime
from activities.services import activity_service
from core.services import paypal_service
from core.util import session_utils
from users.models import Guest

class ActivityDetailView(View):

    def get(self, request, activity_id):
        activity_time = get_object_or_404(ActivityTime, id=activity_id)
        activity = get_object_or_404(Activity, id=activity_time.activity.id)

        activity.start_date = activity_time.date
        activity.start_hour = activity_time.start_hour
        activity.end_hour = activity_time.end_hour

        form = ActivityForm(instance=activity)

        form.setFieldsDisabledProperty(True)
        activity_photo = activity_time.activity.photo
        context = {
            'title': "Detail of an Activity",
            'form': form,
            'is_edit': False,
            'activity_id': activity_time.id,
            'activity_photo': activity_photo,
            'activity': activity_time
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
        result = {"is_refunded": False}
        is_refunded = paypal_service.execute_refound(request, None, activity_id)
        if (is_refunded):
            result["is_refunded"] = True
            activity_service.unsubscribe(activity_id, request)

        return JsonResponse(result)

class ListSubscribedActivitiesView(ListView):
    model = ActivityTime
    template_name = 'activities/list.html'
    context_object_name = 'activities'

    def get_context_data(self, **kwargs):
        context = super(ListSubscribedActivitiesView, self).get_context_data(**kwargs)

        session_utils.set_context_with_activity_session(self.request.session, context)

        return context

    def get_queryset(self):
        today = datetime.datetime.today().date()
        week_forward = today + datetime.timedelta(days=7)
        return Guest.objects.get(id=self.request.user.id).activity_assisted.filter(date__range=(today, week_forward))

class ListAllActivityView(ListView):
    model = ActivityTime
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
        week_forward = today + datetime.timedelta(days=7)
        return ActivityTime.objects.filter(date__range=(today, week_forward))
