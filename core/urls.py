from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^no_permission', views.no_permission, name='no_permission'),
    # PayPal ----------------------------------------------
    url(r'^paypal$', views.paypal_test, name='paypal_test'),
    url(r'^paypal/create-payment$', views.paypal_create_payment, name='create_payment'),
    url(r'^paypal/execute-payment$', views.paypal_execute_payment, name='execute_payment'),
    url(r'^paypal/subscription/execute$', views.paypal_billing_agreement_execute, name='execute_subscription'),
    url(r'^paypal/subscription/cancel$', views.paypal_billing_agreement_cancel, name='cancel_subscription'),

    url(r'dashboard$', views.dashboard, name='dashboard'),
    url(r'dashboard/users$', views.dashboard_users, name='users_dashboard'),
    url(r'deactivate/user/(?P<user_id>\d+)$', views.deactivate_user, name='users_deactivate'),
    url(r'activate/user/(?P<user_id>\d+)$', views.activate_user, name='users_activate'),
    url(r'rankings$', views.rankings, name='rankings'),
    url(r'search$', views.search, name='search'),

]
