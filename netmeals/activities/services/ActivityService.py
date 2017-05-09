from compiler.ast import obj

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


