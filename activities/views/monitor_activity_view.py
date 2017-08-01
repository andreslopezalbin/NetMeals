from urllib.parse import urlparse

from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import resolve
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DeleteView
from  django.views.generic.list import ListView

from activities.forms.ActivityForm import ActivityForm
from activities.models import Activity, ActivityTime
from activities.services import activity_service
from django.shortcuts import get_object_or_404

from core.util import session_utils
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
        if request.session.get(SESSION_ACTIVITY_CREATED_SUCCEEDED):
            del request.session[SESSION_ACTIVITY_CREATED_SUCCEEDED]
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
        activity_photo = activity.photo
        context = {
            'title': title,
            'form': form,
            'is_edit': is_edit,
            'is_new': is_new,
            'activity_id': activity.id,
            'activity_photo': activity_photo
        }
        return render(request, 'activities/view_edit.html', context)

    def post(self, request, activity_id=None):
        form = ActivityForm(request.POST, request.FILES)
        success_msg = ''
        error_msg = ''
        is_edit = False
        is_new = False
        if form.is_valid():
            activity = form.create(request)
            if(activity.id is None or activity.id == ''):
                is_periodocally = form.cleaned_data['is_periodically']
                if(is_periodocally):
                    context = {
                        'form': form
                    }
                    activity_service.save(activity)
                    request.session[SESSION_ACTIVITY_PENDING] = activity.id
                    return render(request, 'activities/new_periodically.html', context)
                else:
                    is_new = True
                    activity_service.save(activity)
                    success_msg = 'Activity saved successfully'
                    request.session[SESSION_ACTIVITY_CREATED_SUCCEEDED] = True
            else:
                is_edit = True
                activity_service.update(activity)
                success_msg = 'Activity updated successfully'
                request.session[SESSION_ACTIVITY_MOD_SUCCEEDED] = True
        else:
            error_msg = 'There was an error validating form'
            activity = Activity()
            if(activity_id):
                is_edit = True
            else:
                is_new = True

        context = {
            'form': form,
            'success_msg': success_msg,
            'error_msg': error_msg,
            'is_edit': is_edit,
            'is_new': is_new,
            'activity_id': activity.id
        }
        if(error_msg):
            return render(request, 'activities/view_edit.html', context)
        else:
            redirect_url = 'my_activities'
            reverse_url = reverse(redirect_url)
            return HttpResponseRedirect(reverse_url)

@method_decorator(group_required('Monitor'), name='dispatch')
class CreateActivityPeriodicallyView(View):

    def post(self, request, activity_id=None):
        success_msg = ''
        error_msg = ''
        if request.session.get(SESSION_ACTIVITY_PENDING):
            activity_id = request.session[SESSION_ACTIVITY_PENDING]

            week_days = request.POST.get('weekDays')
            week_days = week_days.split(",")
            start_date = request.POST.get('start_date')
            start_date = datetime.strptime(start_date, '%d/%m/%Y')
            end_date = request.POST.get('end_date')
            end_date = datetime.strptime(end_date, '%d/%m/%Y')
            start_hour = request.POST.get('start_hour')
            end_hour = request.POST.get('end_hour')

            days = activity_service.datesBeween(start_date, end_date, week_days)
            for day in days:
                activity_time = ActivityTime()
                activity_time.date = day
                activity_time.start_hour = start_hour
                activity_time.end_hour = end_hour
                activity_time.activity_id = activity_id
                activity_time.save()
        else:
            error_msg = 'ERROR'

        redirect_url = 'my_activities'
        reverse_url = reverse(redirect_url)
        return HttpResponseRedirect(reverse_url)

@method_decorator(group_required('Monitor'), name='dispatch')
class ListActivityView(ListView):
    model = Activity
    template_name = 'activities/list.html'
    context_object_name = 'activities'

    def get_context_data(self, **kwargs):
        context = super(ListActivityView, self).get_context_data(**kwargs)

        session_utils.set_context_with_activity_session(self.request.session, context)

        return context

    def get_queryset(self):
        self.owner = User.objects.get(id=self.request.user.id)
        return Activity.objects.filter(owner=self.owner)

@method_decorator(group_required('Monitor'), name='dispatch')
class DeleteActivityView(DeleteView):
    model = Activity

    def get_success_url(self):
        redirect_url = "/"
        self.request.session[SESSION_ACTIVITY_DEL_SUCCEEDED] = True
        if(self.request.META.get('HTTP_REFERER') is not None):
            relative_path = urlparse(self.request.META.get('HTTP_REFERER')).path
            kwargs = {}
            if "detail" in relative_path or "edit" in relative_path:
                redirect_url = 'my_activities'
            else:
                match = resolve(relative_path)
                redirect_url = match.url_name

                if(match.kwargs):
                    kwargs = match.kwargs
        return reverse_lazy(redirect_url, kwargs=kwargs)

    def get_object(self, queryset=None):
        activity = super(DeleteActivityView, self).get_object()
        if not activity.owner.id == self.request.user.id:
            return HttpResponseRedirect("/no-permission")
        return activity
