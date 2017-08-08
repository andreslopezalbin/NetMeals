from django.conf.urls import url
from users.views.GuestViews import RegistrationView

# from users.views.signin import LoginView, logout
from django.contrib.auth.views import login, logout
from users.views.SignupViews import SignupView, SignupRolesView
from users.views.AddRoleView import AddRoleView
from users.views.GuestViews import edit_profile, view_profile

urlpatterns = [
    url(r'^signup$', SignupView.as_view(), name='signup'),
    url(r'^add_role', AddRoleView.as_view(), name='addRole'),
    url(r'^plan/subscription', SignupRolesView.as_view(), name='plan_subscription'),

    url(r'^login$', login, {'template_name': '../templates/login.html'}, name="login"),
    url(r'^logout$', logout, {'next_page': '/'}, name="logout"),
    url(r'^profile/edit$', edit_profile, name='profile_edit'),
    url(r'^profile$', view_profile, name='profile'),
]
