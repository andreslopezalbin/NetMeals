from compiler.ast import obj

from activities.models import Activity


def save(activity):
    activity.save()

def update(activity):
    Activity.objects.filter(id=activity.id).update(
        name=activity.name,
        description=activity.description,
        place=activity.place,
        latitude=activity.latitude,
        longitude=activity.longitude,
        photo=activity.photo,
        start_date=activity.start_date,
        end_date=activity.end_date
    )
