from datetime import timedelta

from activities.models import Activity


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
        start_date=activity.start_date,
        end_date=activity.end_date,
        price_per_person=activity.price_per_person
    )
    if activity.photo is not None:
        Activity.objects.filter(id=activity.id).update(
            photo=activity.photo
        )

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def datesBeween(start_date, end_date, daysOfWeek):
    result = []

    for date in daterange(start_date, end_date):
        if str(date.isoweekday()) in daysOfWeek:
            result.append(date)

    return result


