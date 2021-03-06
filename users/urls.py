from django.conf.urls import url
from users.views.GuestViews import RegistrationView

# from users.views.signin import LoginView, logout
from django.contrib.auth.views import login, logout
from users.views.SignupViews import SignupView
from users.views.AddRoleView import AddRoleView
from users.views.GuestViews import Profile

urlpatterns = [
    url(r'^signup$', SignupView.as_view(), name='signup'),
    url(r'^add_role', AddRoleView.as_view(), name='addRole'),

    url(r'^login$', login, {'template_name': '../templates/login.html'}, name="login"),
    url(r'^logout$', logout, {'next_page': '/'}, name="logout"),
    url(r'^profile', Profile.as_view(), name='profile'),
]
