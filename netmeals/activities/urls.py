from django.conf.urls import url

from activities.views.AddRoleView import AddRoleView
from activities.views.GuestViews import RegistrationView
from activities.views.SignupViews import SignupView
from activities.views.monitor_activity_view import CreateActivityView, ListActivityView

urlpatterns = [
    # Users URLs
    url(r'^register$', RegistrationView.as_view(), name='guest_register'),
    url(r'^signup$', SignupView.as_view(), name='signup'),
    url(r'^add_role', AddRoleView.as_view(), name='addRole'),
    url(r'^activities/(?P<userid>\d+)/new$', CreateActivityView.as_view(), name='new_activity'),
    url(r'^activities/(?P<userid>\d+)/list$', ListActivityView.as_view(), name='my_activities')
]
