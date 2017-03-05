from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signin', views.signin, name='signin'),
    url(r'^logout', views.logout, name='logout'),
    url(r'^no_permission/', views.no_permission, name='no_permission')
]
