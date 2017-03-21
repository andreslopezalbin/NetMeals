from django.conf.urls import url

from activities.views.AddRoleView import AddRoleView
from activities.views.monitor_activity_view import CreateActivityView, ListActivityView

urlpatterns = [
    # Users URLs
    url(r'^add_role', AddRoleView.as_view(), name='addRole'),
    url(r'^activities/(?P<userid>\d+)/new$', CreateActivityView.as_view(), name='new_activity'),
    url(r'^activities/(?P<userid>\d+)/list$', ListActivityView.as_view(), name='my_activities')
]
