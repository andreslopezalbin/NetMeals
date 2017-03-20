from ..models import Activity
from django.views.generic.list import View
from django.shortcuts import render
from core.decorators.user_decorators import group_required


class ActivityFindAllView(View):
    model = Activity

    # @group_required('Monitor')
    def get(self, request):
        activities = Activity.objects.all()
        context = {
            'activities': activities,
        }
        return render(request, 'activitiesList.html', context)
