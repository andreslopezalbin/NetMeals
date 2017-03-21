from django.conf.urls import url
from users.views.GuestViews import RegistrationView

# from users.views.signin import LoginView, logout
from django.contrib.auth.views import login, logout
from users.views.SignupViews import SignupView

urlpatterns = [
    # url(r'^signin', login, name='signin'),
    url(r'^signup$', SignupView.as_view(), name='signup'),
    # url(r'^logout', logout, name='logout'),

    url(r'^login$', login, {'template_name': '../templates/login.html'}),
    url(r'^logout$', logout, {'next_page': '/'}),

    # Guest ==========================================================================
    url(r'^guest/register$', RegistrationView.as_view(), name='guest_register'),
]
