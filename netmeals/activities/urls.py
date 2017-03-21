from django.conf.urls import url

from activities.views.monitor_activity_view import CreateActivityView, ListActivityView
from views.dish_view import findall, findmine

urlpatterns = [
    # Users URLs ----------------------------------------------------------------------
    url(r'^activities/new$', CreateActivityView.as_view(), name='new_activity'),
    url(r'^activities/list$', ListActivityView.as_view(), name='my_activities'),
    # url(r'^activities/(?P<userid>\d+)/list$', ListActivityView.as_view(), name='my_activities')

    # Dish --------------------------------------------------------------------------
    url(r'^dish/findall$', findall, name='all_dishes'),
    url(r'^dish/mydishes$', findmine, name='my_dishes')

]
