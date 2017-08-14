from django.conf.urls import url
from django.contrib.auth.views import login, logout, password_reset, password_reset_done, password_reset_confirm, \
    password_reset_complete

from users.views.AddRoleView import AddRoleView
from users.views.GuestViews import edit_profile, view_profile, edit_about_me
from users.views.SignupViews import SignupView, SignupRolesView

urlpatterns = [
    url(r'^signup$', SignupView.as_view(), name='signup'),
    url(r'^add_role', AddRoleView.as_view(), name='addRole'),
    url(r'^plan/subscription', SignupRolesView.as_view(), name='plan_subscription'),

    url(r'^login$', login, {'template_name': '../templates/login.html'}, name="login"),
    url(r'^logout$', logout, {'next_page': '/'}, name="logout"),
    url(r'^profile/edit$', edit_profile, name='profile_edit'),
    url(r'^profile/edit_about_me$', edit_about_me, name='about_me_edit'),
    url(r'^profile/(?P<username>\w+)', view_profile, name='profile'),

    # ../templates/passwordreset/
    url(r'^password_reset', password_reset,
        {'template_name': '../templates/passwordreset/password_reset_form.html',
         'email_template_name': '../templates/passwordreset/password_reset_email.html'},
        name='password_reset'),
    url(r'^password_reset_done', password_reset_done,
        {'template_name': '../templates/passwordreset/password_reset_done.html'},
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', password_reset_confirm,
        {'template_name': '../templates/passwordreset/password_reset_confirm.html'},
        name='password_reset_confirm'
        ),
    url(r'^reset/done', password_reset_complete,
        {'template_name': '../templates/passwordreset/password_reset_complete.html'},
        name='password_reset_complete'),
]
