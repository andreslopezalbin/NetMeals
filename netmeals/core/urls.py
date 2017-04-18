from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^no_permission', views.no_permission, name='no_permission'),
    url(r'^prueba$', views.prueba, name='prueba')
    ,
]
