from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from activities.views.activity_view import ListAllActivityView, ActivityDetailView, ActivitySubscriptionView, \
    ListSubscribedActivitiesView, ActivityUnsubscriptionView
from activities.views.monitor_activity_view import CreateActivityView, ListActivityView, DeleteActivityView, \
    CreateActivityPeriodicallyView
from activities.views.dish_view import findall, findmine, create, edit, details, schedule, delete, DishUnsubscriptionView, DishSubscriptionView


urlpatterns = [
    # Users URLs ----------------------------------------------------------------------
    url(r'^activities/(?P<activity_id>\d+)/detail$', ActivityDetailView.as_view(), name='activity_detail'),
    url(r'^activities/(?P<activity_id>\d+)/edit$', CreateActivityView.as_view(), name='activity_edit'),
    url(r'^activities/(?P<pk>\d+)/delete$', DeleteActivityView.as_view(), name='activity_delete'),
    url(r'^activities/(?P<activity_id>\d+)/subscribe', login_required(ActivitySubscriptionView.as_view()), name='activity_subscribe'),
    url(r'^activities/(?P<activity_id>\d+)/unsubscribe', login_required(ActivityUnsubscriptionView.as_view()), name='activity_unsubscribe'),
    url(r'^activities/new$', CreateActivityView.as_view(), name='new_activity'),
    url(r'^activities/new_periodically$', CreateActivityPeriodicallyView.as_view(), name='new_activity_periodically'),
    url(r'^activities/list$', ListActivityView.as_view(), name='my_activities'),
    url(r'^activities/subscribed$', ListSubscribedActivitiesView.as_view(), name='my_subscriptions'),
    url(r'^activities/findall$', ListAllActivityView.as_view(), name='all_activities'),
    # url(r'^activities/(?P<userid>\d+)/list$', ListActivityView.as_view(), name='my_activities')

    # Dish --------------------------------------------------------------------------
    url(r'^dish/findall$', findall, name='all_dishes'),
    url(r'^dish/mydishes$', findmine, name='my_dishes'),
    url(r'^dish/new$', create, name='new_dish'),
    url(r'^dish/details/(?P<dish_id>[0-9]+)$', details, name='details_dish'),
    url(r'^dish/edit/(?P<dish_id>[0-9]+)$', edit, name='edit_dish'),
    url(r'^dish/delete/(?P<dish_id>[0-9]+)$', delete, name='delete_dish'),
    url(r'^dish/schedule$', schedule, name='schedule'),
    url(r'^dish/(?P<dish_id>\d+)/subscribe', login_required(DishSubscriptionView.as_view()), name='dish_subscribe'),
    url(r'^dish/(?P<dish_id>\d+)/unsubscribe', login_required(DishUnsubscriptionView.as_view()), name='dish_unsubscribe'),


]
