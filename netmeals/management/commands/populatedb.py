# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Permission
from django.contrib.auth.models import Group

from core.models import Feedback, IncomingPayment, OutcomingPayment
from core.services import paypal_service
from activities.models import Activity, Dish, DishFeedback, ActivityTime, ActivityFeedback
from users.models import Guest, Chef, Monitor, Manager, Plan
from django.contrib.contenttypes.models import ContentType

from users.util.users_constants import PLAN_FREE, PLAN_LITE, PLAN_PREMIUM


class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def _migrate(self):
        # Drop all tables
        print('Dropping tables...')
        IncomingPayment.objects.all().delete()
        OutcomingPayment.objects.all().delete()
        User.objects.all().delete()
        Dish.objects.all().delete()
        Activity.objects.all().delete()
        ActivityTime.objects.all().delete()
        Feedback.objects.all().delete()
        Plan.objects.all().delete()

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
            name=PLAN_FREE,
            description='NetMeals Free Plan'
        )
        free_plan.save()

        premium_plan = None
        premium_plan_id = paypal_service.create_premium_billing_plan()
        if (premium_plan_id is not None):
            premium_plan = Plan(
                paypal_plan_id=premium_plan_id,
                amount=14.99,
                name=PLAN_PREMIUM,
                description='NetMeals Premium Plan'
            )
            premium_plan.save()

        lite_plan = None
        lite_plan_id = paypal_service.create_lite_billing_plan()
        if (lite_plan_id is not None):
            lite_plan = Plan(
                paypal_plan_id=lite_plan_id,
                amount=9.99,
                name=PLAN_LITE,
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
        admin_2.set_password('@desarrollo2017')
        admin_2.is_staff = True
        admin_2.is_superuser = True
        admin_2.save()

        print('Admins created...Ok')

        admin_admin = User(
            username='admin',
            email='admin@admin.com',
            date_joined='2016-9-5')
        admin_admin.set_password('@desarrollo2017')
        admin_admin.is_staff = True
        admin_admin.is_superuser = True
        admin_admin.save()

        print('Admins created...Ok')

        # ==================================================================================================
        # ==================================================================================================

        guest1 = Guest(
            username='Manel',
            email='guest1@guest1.com',
            first_name='guest1',
            date_joined='2016-10-5'
        )
        guest1.set_password('@desarrollo2017')
        guest1.save()
        guest1.groups.add(Group.objects.get(name='Guest'))

        guest2 = Guest(
            username='carlos',
            email='carlos@netmeals.com',
            first_name='carlos',
            date_joined='2016-11-13'
        )
        guest2.set_password('@desarrollo2017')
        guest2.save()
        guest2.groups.add(Group.objects.get(name='Chef'))
        print('Guests created...Ok')

        guest3 = Guest(
            username='maria',
            email='guest3@guest3.com',
            first_name='Maria',
            date_joined='2016-12-5'
        )
        guest3.set_password('@desarrollo2017')
        guest3.save()
        guest3.groups.add(Group.objects.get(name='Guest'))

        guest4 = Guest(
            username='virginia',
            email='guest4@guest4.com',
            first_name='Virginia',
            date_joined='2017-1-5'
        )
        guest4.set_password('@desarrollo2017')
        guest4.save()
        guest4.groups.add(Group.objects.get(name='Guest'))

        guest5 = Guest(
            username='guest5',
            email='guest5@guest5.com',
            first_name='Matt',
            date_joined='2017-2-5'
        )
        guest5.set_password('@desarrollo2017')
        guest5.save()
        guest5.groups.add(Group.objects.get(name='Guest'))

        # ==================================================================================================
        # ==================================================================================================
        andres = Chef(
            username='andres',
            email='andres@netmeals.com',
            first_name='Andrés',
            last_name='López Albín',
            date_joined='2017-3-5',
            photo="/media/profiles/andres.png",
            birthday='1993-01-04'
        )
        andres.set_password('@desarrollo2017')
        andres.save()
        andres.groups.add(Group.objects.get(name='Chef'))
        andres.user_permissions.add(Permission.objects.get(name='Free'))

        chef1 = Chef(
            username='cocinero',
            email='chef1@chef1.com',
            first_name='Manolo',
            date_joined='2017-3-5',
            photo="/media/profiles/chef1.ico",
            birthday='1993-9-29'
        )
        chef1.set_password('@desarrollo2017')
        chef1.save()
        chef1.groups.add(Group.objects.get(name='Chef'))
        chef1.user_permissions.add(Permission.objects.get(name='Free'))

        chef2 = Chef(
            username='chef1',
            email='chef2@chef2.com',
            first_name='Pepi',
            date_joined='2017-4-5',
            birthday='2000-7-29',
            photo="/media/profiles/chef2.jpg"
        )
        chef2.set_password('@desarrollo2017')
        chef2.save()
        chef2.groups.add(Group.objects.get(name='Chef'))
        chef2.user_permissions.add(Permission.objects.get(name='Free'))

        print('Chefs created...Ok')

        # ==================================================================================================
        # ==================================================================================================

        monitor1 = Monitor(
            username='antmarpen',
            email='antmarpen@netmeals.com',
            first_name='Antonio',
            date_joined='2017-5-5',
            photo="/media/profiles/monitor1.jpg"
        )
        monitor1.set_password('@desarrollo2017')
        monitor1.save()
        monitor1.groups.add(Group.objects.get(name='Monitor'))
        monitor1.user_permissions.add(Permission.objects.get(name='Free'))

        monitor2 = Monitor(
            username='sormaria',
            email='sormaria@netmeals.com',
            first_name='Sor',
            last_name='Maria',
            date_joined='2017-6-5',
            photo='/media/profiles/sormaria.jpg'
        )
        monitor2.set_password('@desarrollo2017')
        monitor2.save()
        monitor2.groups.add(Group.objects.get(name='Monitor'))
        monitor2.user_permissions.add(Permission.objects.get(name='Lite'))

        print('Monitors created...Ok')

        # ==================================================================================================
        # ==================================================================================================



        # ==================================================================================================
        # ==================================================================================================
        #

        activity1 = Activity(
            name='Shushi',
            short_description='El mejor itamae para enseñarte el mejor Sushi de la ciudad',
            description='Os enseñaré a preparar shushi, son su alga nori, salmón, aguacate y todo lo que le quieras poner! ',
            place='Carlos Marx, 10, 6b, Sevilla',
            photo='/media/activities/sushi.jpg',
            latitude=37.383143499999996,
            longitude=-5.9492486,
            price_per_person=6,
            owner=monitor1
        )
        activity1.save()

        activitytime1 = ActivityTime(activity=activity1, date='2017-9-15', start_hour="17:00:00", end_hour='18:00:00')
        activitytime1.save()
        activitytime1.assistants.add(andres)

        activity2 = Activity(
            name='Tacos mexicanos',
            short_description='Tacos para todos!',
            description='Vamos a preparar los mejores tacos picantes de tijuana! ',
            place='Carlos Marx, 10, 6b, Sevilla',
            photo='/media/activities/tacos.png',
            latitude=37.383143499999996,
            longitude=-5.9492486,
            price_per_person=6,
            owner=monitor1
        )
        activity2.save()

        activitytime2 = ActivityTime(activity=activity2, date='2017-9-12', start_hour="17:00:00", end_hour='19:00:00')
        activitytime2.save()
        activitytime2.assistants.add(guest1)
        activitytime2.assistants.add(guest2)
        activitytime2.save()

        activitytime3 = ActivityTime(activity=activity2, date='2017-9-17', start_hour="12:00:00", end_hour='13:00:00')
        activitytime3.save()
        activitytime3.assistants.add(andres)
        activitytime3.assistants.add(guest3)
        activitytime3.save()

        activity3 = Activity(
            name='Pestiños',
            short_description='El pestiño es un dulce navideño o de Semana Santa, típico de Andalucía y otras zonas de España',
            description='Esta receta tradicional de dulces es ideal tanto para desayunar como para merendar o tomar de postre en las ocasiones especiales. Al preparar esta receta de pestiños siempre debemos tener cuidado con la miel y no pasarnos con ciertos ingredientes.',
            place='Calle San José, 4, 41004 Sevilla',
            photo='/media/activities/pestiños.jpg',
            latitude=37.3878483,
            longitude=-5.9896655,
            price_per_person=4,
            owner=monitor2
        )
        activity3.save()

        activitytime3 = ActivityTime(activity=activity3, date='2017-9-16', start_hour="12:00:00", end_hour='13:00:00')
        activitytime3.save()
        activitytime3.assistants.add(guest1)
        activitytime3.assistants.add(guest2)
        activitytime3.save()

        activitytime4 = ActivityTime(activity=activity3, date='2017-9-18', start_hour="12:00:00", end_hour='13:00:00')
        activitytime4.save()
        activitytime4.assistants.add(andres)
        activitytime4.assistants.add(guest3)
        activitytime4.save()

        activitytime5 = ActivityTime(activity=activity3, date='2017-9-19', start_hour="12:00:00", end_hour='13:00:00')
        activitytime5.save()
        activitytime5.assistants.add(andres)
        activitytime5.assistants.add(guest3)
        activitytime5.save()

        activity4 = Activity(
            name='Curso de enología',
            short_description='Fórmate profesionalmente en el mundo de la enología y aprende desde las técnicas de la cata de vino ',
            description='Con la realización del curso de enología: Distinguirás los diferentes tipos de vino e interpretarás correctamente su etiquetado. Dominarás todos los aspectos relacionados con el cultivo de la vid, su anatomía y su ciclo de vida.Conocerás las influencias del suelo y del clima en la viña y su fruto.Aprenderás todas las técnicas para catar y maridar vinos.',
            place='Calle San José, 4, 41004 Sevilla',
            photo='/media/activities/enologia.jpg',
            latitude=37.3878483,
            longitude=-5.9896655,
            price_per_person=4,
            owner=monitor2
        )
        activity4.save()

        activitytime6 = ActivityTime(activity=activity4, date='2017-9-20', start_hour="12:00:00", end_hour='13:00:00')
        activitytime6.save()
        activitytime6.assistants.add(guest1)
        activitytime6.assistants.add(guest2)
        activitytime6.save()

        print('Activities... ok')

        # ==================================================================================================
        #  Dish
        # ==================================================================================================

        dish1 = Dish(name='Menestra', description='dish1Description', date='2017-09-20', hour='12:00', owner=chef1,
                     latitude=37.3730406,
                     longitude=-5.961418, place='Calle Aníbal González, 17, Sevilla',
                     max_assistants=3, contribution=5.6,
                     photo='/media/dish/dish1.jpg',
                     short_description="La menestra de verduras es un plato muy completo, repleto de vitaminas, minerales")
        dish1.save()
        dish1.assistants.add(guest1)
        dish1.assistants.add(guest2)

        dish2 = Dish(name='Huevos a la flamenca',
                     description='Los huevos a la flamenca, gloria bendita de las tierras andaluzas, deberían ser plato del día en todos los bares de España. Así a lo tonto son un señor plato combinado metido en una cazuelita, con su parte de verduritas, su miaja de carne y un núcleo de huevo donde untar el pan sin parar.',
                     date='2017-09-15', hour='13:00', owner=chef1,
                     latitude=37.3817407,
                     longitude=-5.96297, place='Calle Padre Pedro Ayala, 53',
                     max_assistants=3, contribution=4.0,
                     photo='/media/dish/dish2.jpg',
                     short_description="Los huevos a la flamenca, gloria bendita de las tierras andaluzas, deberían ser plato del día en todos los bares de España")
        dish2.save()
        dish2.assistants.add(chef2)
        dish3 = Dish(name='Noodles de verdura',
                     description='Este plato os puede recordar un poco a los típicos tallarines fritos con verduras de los restaurantes chinos... pero os aseguro que están mucho más buenos y son más sanos, porque controlamos la cantidad de grasa, de sal y los ingredientes que llevan',
                     date='2017-03-25', hour='14:00', owner=chef2,
                     latitude=37.3817,
                     longitude=-5.974244, place='Calle Padre Campelo, 4',
                     max_assistants=1, contribution=2.0,
                     photo='/media/dish/dish3.jpg',
                     short_description="Aquí os presento mi versión más sana y casera de los noodles orientales")
        dish3.save()
        dish4 = Dish(name='Salmón al limón', description='dish4Description', date='2017-09-29', hour='14:00',
                     owner=chef2,
                     latitude=37.3741023,
                     longitude=-6.0002047, place='Calle Fernando IV, 34',
                     max_assistants=5, contribution=5.0,
                     photo='/media/dish/dish4.jpg',
                     short_description="Es una receta ligh y una salsa muy suave delicioso")
        dish4.save()
        dish5 = Dish(name='Tortitas', description='dish5Description', date='2017-9-25', hour='15:00', owner=chef2,
                     latitude=37.3784899,
                     longitude=-6.0035505, place='Calle Esperanza de Triana, 57',
                     max_assistants=10, contribution=3.6,
                     short_description="Desayuno al estido USA con tortitas, sirope y café aguado",
                     photo='/media/dish/tortitas.jpg',
                     )
        dish5.save()

        print('Dishes... Ok')

        # ==================================================================================================
        #  Dish
        # ==================================================================================================

        dish_feedback1 = DishFeedback(score=5,
                                      dish=dish1,
                                      comment="Manolo es muy buen huesped, la menestra esta de escandalo",
                                      commentator=andres,
                                      commented=chef1)
        dish_feedback1.save()

        dish_feedback2 = DishFeedback(score=2,
                                      dish=dish2,
                                      comment="Le pongo un 2 porque la comida estaba decente, pero Manolo no me cayó bien",
                                      commentator=chef2,
                                      commented=chef1)
        dish_feedback2.save()

        dish_feedback3 = DishFeedback(score=4,
                                      dish=dish1,
                                      comment="Buen rato con manolo y los demás comensales, buena comida",
                                      commentator=monitor1,
                                      commented=chef1)
        dish_feedback3.save()

        print('DishesFeedback... Ok')

        activity_feedback1 = ActivityFeedback(score=5,
                                              activity=activity1,
                                              comment="Soy un pro del sushi ahora mismo!! :D ",
                                              commentator=andres,
                                              commented=monitor1)
        activity_feedback1.save()

        activity_feedback2 = ActivityFeedback(score=5,
                                              activity=activity3,
                                              comment="Estos pestiños estan riquísimos!",
                                              commentator=monitor1,
                                              commented=monitor2)
        activity_feedback2.save()

        activity_feedback3 = ActivityFeedback(score=5,
                                              activity=activity3,
                                              comment="Sor María es encantadora y muy buena profesora",
                                              commentator=andres,
                                              commented=monitor2)
        activity_feedback3.save()

        print('Populating database...OK\n'
              'Ready to use!')

    def handle(self, *args, **options):
        self._migrate()
