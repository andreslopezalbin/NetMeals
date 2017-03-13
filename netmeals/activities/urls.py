from django.conf.urls import url
from activities.views.GuestViews import RegistrationView
from activities.views.SignupViews import SignupView

urlpatterns = [
    # Users URLs
    url(r'^register$', RegistrationView.as_view(), name='guest_register'),
    url(r'^signup$', SignupView.as_view(), name='signup')
]
