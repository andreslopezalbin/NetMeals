from django.contrib import admin

from activities.models import Activity, Dish, ActivityTime, ActivityFeedback, DishFeedback

# Register your models here.
admin.site.register(Activity)
admin.site.register(Dish)
admin.site.register(ActivityTime)
admin.site.register(ActivityFeedback)
admin.site.register(DishFeedback)



