import datetime
import random
import json
from urllib.parse import urlparse

from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from  django.views.generic.list import ListView
from django.shortcuts import get_object_or_404

from activities.forms.ActivityFeedbackForm import ActivityFeedbackForm
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

        if (not context['activities']):
            context['activities'] = []

        session_utils.set_context_with_activity_session(self.request.session, context)

        return context

    def get_queryset(self):
        today = datetime.datetime.today().date()
        week_forward = today + datetime.timedelta(days=7)
        return ActivityTime.objects.filter(date__range=(today, week_forward))


# activity_id es realmente el id del activitytime
def activity_feedback(request, activity_id, activitytime_id):
    activity = Activity.objects.get(id=activity_id)
    if request.method == "POST":
        form = ActivityFeedbackForm(request.POST)
        if form.is_valid():
            activityfeedback = form.save(commit=False)
            activityfeedback.activity_id = activity.id
            activityfeedback.commentator = request.user.guest
            activityfeedback.commented_id = activity.owner.id
            activityfeedback.save()
            return redirect('activity_detail', activity_id=activitytime_id)
    else:
        form = ActivityFeedbackForm()
    return render(request, 'activities/feedback.html', {'form': form})


def activity_schedule(request):
    if request.method == "GET" and request.user.groups.filter(name='Monitor').exists():
        activities = request.user.guest.monitor.activity_set.all()
        activitytimes = []
        for activity in activities:
            for activitytime in activity.activitytime_set.all():
                activitytimes.append(activitytime)

        user_language = request.LANGUAGE_CODE
        today = datetime.date.today()
        items = []
        colors = ['blue', 'champagne', 'grey', 'red', 'pink', 'green', 'salmon']
        for i, activitytime in enumerate(activitytimes):
            item = {'title': activitytime.activity.name,
                    'url': str(activitytime.activity.id) + '/detail',
                    'start': str(activitytime.date) + " " + str(activitytime.start_hour),
                    'end': str(activitytime.date) + " " + str(activitytime.end_hour),
                    'color': colors[random.randrange(0, len(colors))]}

            items.append(item)
        data = json.dumps(items)
        context = {'items': data, 'language': user_language, 'today': today}
        return render(request, '../templates/activities/scheduler.html', context)
