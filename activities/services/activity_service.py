from datetime import timedelta

from django.shortcuts import get_object_or_404
from activities.models import Activity, ActivityTime
from users.models import Guest


def save(activity):
    activity.save()


def update(activity):
    Activity.objects.filter(id=activity.id).update(
        name=activity.name,
        short_description=activity.short_description,
        description=activity.description,
        place=activity.place,
        latitude=activity.latitude,
        longitude=activity.longitude,
        price_per_person=activity.price_per_person
    )
    if activity.photo is not None:
        Activity.objects.filter(id=activity.id).update(
            photo=activity.photo
        )

def update_activity_time(activity_time):
    ActivityTime.objects.filter(id=activity_time.id).update(
        date=activity_time.date,
        start_hour=activity_time.start_hour,
        end_hour=activity_time.end_hour
    )

def subscribe(activity_id, request):
    activity_time = get_object_or_404(ActivityTime, id=activity_id)
    guest = Guest.objects.get(id=request.user.id)

    if (activity_time.activity.owner_id != request.user.id):
        activity_time.assistants.add(guest)

def unsubscribe(activity_id, request):
    activity_time = get_object_or_404(ActivityTime, id=activity_id)
    guest = Guest.objects.get(id=request.user.id)

    if (activity_time.activity.owner_id != request.user.id):
        activity_time.assistants.remove(guest)

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def datesBeween(start_date, end_date, daysOfWeek):
    result = []

    for date in daterange(start_date, end_date):
        if str(date.isoweekday()) in daysOfWeek:
            result.append(date)

    return result


