from django.db import connection

from activities.models import Activity, Dish, ActivityTime


def search_by_proximity_with_distance(latitude, longitude, miles_distance):
    activities = []
    dishes = []
    latitude_float = float(latitude)
    longitude_float = float(longitude)
    with connection.cursor() as cursor:
        cursor.execute("CALL geodist(" + format(latitude_float, '.20f') + ", " + format(longitude_float, '.20f') + ", " + str(miles_distance) + ")")
        for row in cursor.fetchall():
            meters = row[2] * 1000 * 1.609344
            if(meters < 1):
                meters = 0

            meters_str = format(meters, '.2f')

            if(row[0] == "activity"):
                activity_time = ActivityTime.objects.get(id=row[1])
                if(activity_time is not None):
                    tupla = (activity_time, meters_str,)
                    activities.append(tupla)
            elif(row[0] == "dish"):
                dish = Dish.objects.get(id=row[1])
                if(dish is not None):
                    tupla = (dish, meters_str,)
                    dishes.append(tupla)

    return activities, dishes


def search_by_proximity(latitude, longitude):
    return search_by_proximity_with_distance(latitude, longitude, 10)