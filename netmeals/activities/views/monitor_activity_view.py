from django.utils.decorators import method_decorator
from django.views import View
from  django.views.generic.list import ListView
from django.shortcuts import render
from django.http import HttpResponseRedirect

from activities.models import Activity
from django.contrib.auth.models import User
from activities.forms.ActivityForm import ActivityForm
from activities.services import ActivityService
from core.decorators.user_decorators import group_required


@method_decorator(group_required('Monitor'), name='dispatch')
class CreateActivityView(View):

    def get(self, request, userid):
        form = ActivityForm()
        context = {
            'form': form,
        }
        return render(request, 'activities/view_edit.html', context)

    def post(self, request, userid):
        form = ActivityForm(request.POST)
        if long(userid) != request.user.id:
            return HttpResponseRedirect("no_permission.html")
        if form.is_valid():
            activity = form.create(request)
            ActivityService.save(activity)
            return HttpResponseRedirect("/")
        else:
            context = {
                'form': form,
            }
            return render(request, 'activities/view_edit.html', context)

class ListActivityView(ListView):
    model = Activity
    template_name = 'activities/list.html'
    context_object_name = 'list'

    def get_queryset(self):
        self.owner = User.objects.get(id=self.kwargs['userid'])
        return Activity.objects.filter(owner=self.owner)