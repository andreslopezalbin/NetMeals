from django.conf.urls import url

from activities.views.monitor_activity_view import CreateActivityView, ListActivityView

urlpatterns = [
    # Users URLs
    url(r'^new$', CreateActivityView.as_view(), name='new_activity'),
    url(r'^list$', ListActivityView.as_view(), name='my_activities')
    # url(r'^activities/(?P<userid>\d+)/list$', ListActivityView.as_view(), name='my_activities')
]
