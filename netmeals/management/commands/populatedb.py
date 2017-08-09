# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Permission
from django.contrib.auth.models import Group
from activities.models import Activity, Dish, DishFeedback
from users.models import Guest, Chef, Monitor, Manager, Plan
from django.contrib.contenttypes.models import ContentType

from users.util.users_constants import PLAN_FREE, PLAN_LITE, PLAN_PREMIUM


class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def _migrate(self):
        # Drop all tables
        print('Dropping tables...')

        User.objects.all().delete()
        Activity.objects.all().delete()
        Dish.objects.all().delete()
        DishFeedback.objects.all().delete()

        print('Dropping tables...OK')
        print('Populating database...')

        # ==================================================================================================
        # ==================================================================================================

        Group.objects.get_or_create(name='Guest')
        Group.objects.get_or_create(name='Monitor')
        Group.objects.get_or_create(name='Chef')
        Group.objects.get_or_create(name='Manager')
        print('Groups created...Ok')

        # ==================================================================================================
        #  Billing Plans
        # ==================================================================================================
        free_plan = Plan(
            paypal_plan_id='',
            amount=0.00,
            name = PLAN_FREE,
            description='NetMeals Free Plan'
        )
        free_plan.save()

        premium_plan = None
        premium_plan_id = paypal_service.create_premium_billing_plan()
        if (premium_plan_id is not None):
            premium_plan = Plan(
                paypal_plan_id=premium_plan_id,
                amount=14.99,
                name = PLAN_PREMIUM,
                description='NetMeals Premium Plan'
            )
            premium_plan.save()

        lite_plan = None
        lite_plan_id = paypal_service.create_lite_billing_plan()
        if (lite_plan_id is not None):
            lite_plan = Plan(
                paypal_plan_id=lite_plan_id,
                amount=9.99,
                name = PLAN_LITE,
                description='NetMeals Lite Plan'
            )
            lite_plan.save()

        print('Plans... Ok')

        plan = ContentType.objects.get_for_model(Plan)
        Permission.objects.get_or_create(codename='free',
                                         name='Free',
                                         content_type=plan)
        Permission.objects.get_or_create(codename='lite',
                                         name='Lite',
                                         content_type=plan)
        Permission.objects.get_or_create(codename='premium',
                                         name='Premium',
                                         content_type=plan)
        print('Permissions created...Ok')

        # ==================================================================================================
        # ==================================================================================================

        admin_2 = User(
            username='admin2',
            email='admin2@admin2.com',
            date_joined='2016-9-5')
        admin_2.set_password('admin2')
        admin_2.is_staff = True
        admin_2.is_superuser = True
        admin_2.save()

        print('Admins created...Ok')

        admin_admin = User(
            username='admin',
            email='admin@admin.com',
            date_joined='2016-9-5')
        admin_admin.set_password('admin')
        admin_admin.is_staff = True
        admin_admin.is_superuser = True
        admin_admin.save()

        print('Admins created...Ok')

        # ==================================================================================================
        # ==================================================================================================

        guest1 = Guest(
            username='guest1',
            email='guest1@guest1.com',
            first_name='guest1',
            date_joined='2016-10-5',
            photo='/media/profiles/guest1.jpg',
        )
        guest1.set_password('guest1')
        guest1.save()
        guest1.groups.add(Group.objects.get(name='Guest'))

        guest2 = Guest(
            username='guest2',
            email='guest2@guest2.com',
            first_name='guest2',
            date_joined='2016-11-13'
        )
        guest2.set_password('guest2')
        guest2.save()
        guest2.groups.add(Group.objects.get(name='Guest'))
        print('Guests created...Ok')

        guest3 = Guest(
            username='guest3',
            email='guest3@guest3.com',
            first_name='guest3',
            date_joined='2016-12-5'
        )
        guest3.set_password('guest3')
        guest3.save()
        guest3.groups.add(Group.objects.get(name='Guest'))

        guest4 = Guest(
            username='guest4',
            email='guest4@guest4.com',
            first_name='guest4',
            date_joined='2017-1-5'
        )
        guest4.set_password('guest4')
        guest4.save()
        guest4.groups.add(Group.objects.get(name='Guest'))

        guest5 = Guest(
            username='guest5',
            email='guest5@guest5.com',
            first_name='guest5',
            date_joined='2017-2-5'
        )
        guest5.set_password('guest5')
        guest5.save()
        guest5.groups.add(Group.objects.get(name='Guest'))

        # ==================================================================================================
        # ==================================================================================================
        andres = Chef(
            username='andres',
            email='andres@chef.com',
            first_name='Andrés',
            last_name='López Albín',
            date_joined='2017-3-5',
            photo="/media/profiles/andres.png",
            birthday='1993-01-04'
        )
        andres.set_password('andres')
        andres.save()
        andres.groups.add(Group.objects.get(name='Chef'))
        andres.user_permissions.add(Permission.objects.get(name='Free'))

        chef1 = Chef(
            username='chef1',
            email='chef1@chef1.com',
            first_name='chef1',
            date_joined='2017-3-5',
            photo="/media/profiles/chef1.ico",
            birthday='1993-9-29'
        )
        chef1.set_password('chef1')
        chef1.save()
        chef1.groups.add(Group.objects.get(name='Chef'))
        chef1.user_permissions.add(Permission.objects.get(name='Free'))

        chef2 = Chef(
            username='chef2',
            email='chef2@chef2.com',
            first_name='chef2',
            date_joined='2017-4-5',
            birthday='2000-7-29',
            photo="/media/profiles/chef2.jpg"
        )
        chef2.set_password('chef2')
        chef2.save()
        chef2.groups.add(Group.objects.get(name='Chef'))
        chef2.user_permissions.add(Permission.objects.get(name='Free'))

        print('Chefs created...Ok')

        # ==================================================================================================
        # ==================================================================================================

        monitor1 = Monitor(
            username='monitor1',
            email='monitor1@monitor1.com',
            first_name='monitor1',
            date_joined='2017-5-5',
            photo="/media/profiles/monitor1.jpg"
        )
        monitor1.set_password('monitor1')
        monitor1.save()
        monitor1.groups.add(Group.objects.get(name='Monitor'))
        monitor1.user_permissions.add(Permission.objects.get(name='Free'))

        monitor2 = Monitor(
            username='monitor2',
            email='monitor2@monitor2.com',
            first_name='monitor2',
            date_joined='2017-6-5',
            photo='/media/profiles/monitor2.png'
        )
        monitor2.set_password('monitor2')
        monitor2.save()
        monitor2.groups.add(Group.objects.get(name='Monitor'))
        monitor2.user_permissions.add(Permission.objects.get(name='Free'))

        print('Monitors created...Ok')

        # ==================================================================================================
        # ==================================================================================================

        manager1 = Manager(
            username='manager1',
            email='manager1@manager1.com',
            first_name='manager1',
            date_joined='2017-7-5'
        )
        manager1.set_password('manager1')
        manager1.save()
        manager1.groups.add(Group.objects.get(name='Manager'))
        manager1.user_permissions.add(Permission.objects.get(name='Free'))

        manager2 = Manager(
            username='manager2',
            email='manager1@manager2.com',
            first_name='manager2',
            date_joined='2017-8-5'
        )
        manager2.set_password('manager2')
        manager2.save()
        manager2.groups.add(Group.objects.get(name='Manager'))
        manager2.user_permissions.add(Permission.objects.get(name='Free'))

        print('Managers created...Ok')

        # ==================================================================================================
        # ==================================================================================================

        activity1 = Activity(
            name='activity1',
            description='activity1Description',
            place='activity1Place',
            latitude=10.0,
            longitude=10.0,
            start_date='2017-3-5',
            price_per_person=6,
            end_date='2017-7-29',
            owner=monitor1
        )
        activity1.save()
        activity1.assistants.add(guest1)
        activity1.assistants.add(guest2)

        activity2 = Activity(
            name='activity2',
            description='activity2Description',
            place='activity2Place',
            latitude=10.0,
            longitude=10.0,
            start_date='2010-3-15',
            end_date='2017-7-29',
            price_per_person=6,
            owner=monitor2,
        )
        activity2.save()
        activity2.assistants.add(guest1)

        print('Activities... ok')

        # ==================================================================================================
        #  Dish
        # ==================================================================================================

        dish1 = Dish(name='dish1', description='dish1Description', date='2017-02-5', hour='12:00', owner=chef1,
                     max_assistants=3, contribution=5.6,
                     photo='/media/dish/dish1.jpg',
                     short_description="esto es una descripción de 140 caracteres, esto es una descripción de 140 caracteres, esto es una descripción de 140 caracteres, y así......")
        dish1.save()
        dish1.assistants.add(guest1)
        dish1.assistants.add(guest2)
        dish2 = Dish(name='dish2', description='dish2Description', date='2017-03-15', hour='13:00', owner=chef1,
                     max_assistants=3, contribution=4.0,
                     photo='/media/dish/dish2.jpg',
                     short_description="esto es una descripción de 140 caracteres, esto es una descripción de 140 caracteres, esto es una descripción de 140 caracteres, y así......")
        dish2.save()
        dish2.assistants.add(chef2)
        dish3 = Dish(name='dish3', description='dish3Description', date='2017-03-25', hour='14:00', owner=chef2,
                     max_assistants=1, contribution=2.0,
                     photo='/media/dish/dish3.jpg',
                     short_description="esto es una descripción de 140 caracteres, esto es una descripción de 140 caracteres, esto es una descripción de 140 caracteres, y así......")
        dish3.save()
        dish4 = Dish(name='dish4', description='dish4Description', date='2017-08-29', hour='14:00', owner=chef2,
                     max_assistants=5, contribution=5.0,
                     photo='/media/dish/dish4.jpg',
                     short_description="esto es una descripción de 140 caracteres, esto es una descripción de 140 caracteres, esto es una descripción de 140 caracteres, y así......")
        dish4.save()
        dish5 = Dish(name='dish5', description='dish5Description', date='2017-8-25', hour='15:00', owner=chef2,
                     max_assistants=10, contribution=3.6,
                     short_description="esto es una descripción de 140 caracteres, esto es una descripción de 140 caracteres, esto es una descripción de 140 caracteres, y así......")
        dish5.save()

        print('Dishes... Ok')

        # ==================================================================================================
        #  Dish
        # ==================================================================================================

        dish_feedback1 = DishFeedback(score=5,
                                      dish=dish1,
                                      comment="esto es una descripción de 140 caracteres, esto es una descripción de 140 caracteres, esto es una descripción de 140 caracteres, y así......",
                                      commentator=andres,
                                      commented=chef1)
        dish_feedback1.save()

        dish_feedback2 = DishFeedback(score=2,
                                      dish=dish2,
                                      comment="esto es una descripción de 140 caracteres, esto es una descripción de 140 caracteres, esto es una descripción de 140 caracteres, y así......",
                                      commentator=chef2,
                                      commented=chef1)
        dish_feedback2.save()

        dish_feedback3 = DishFeedback(score=1,
                                      dish=dish1,
                                      comment="esto es una descripción de 140 caracteres, esto es una descripción de 140 caracteres, esto es una descripción de 140 caracteres, y así......",
                                      commentator=monitor1,
                                      commented=chef1)
        dish_feedback3.save()

        print('DishesFeedback... Ok')
        print('Populating database...OK\n'
              'Ready to use!')

    def handle(self, *args, **options):
        self._migrate()
