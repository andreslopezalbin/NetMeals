from django.conf.urls import url
from activities.views.ActivityViews import ActivityFindAllView

urlpatterns = [
    # Users URLs

    url(r'^findall$', ActivityFindAllView.as_view(), name='findAll')
]
