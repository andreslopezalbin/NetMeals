# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Permission
from django.contrib.auth.models import Group
from activities.models import Local, Activity
from users.models import Guest, Chef, Monitor, Manager, Plan
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def _migrate(self):
        # Drop all tables
        print('Dropping tables...')

        User.objects.all().delete()
        Activity.objects.all().delete()
        Local.objects.all().delete()

        print('Dropping tables...OK')
        print('Populating database...')

        # ==================================================================================================
        # ==================================================================================================

        Group.objects.get_or_create(name='Guest')
        Group.objects.get_or_create(name='Monitor')
        Group.objects.get_or_create(name='Chef')
        Group.objects.get_or_create(name='Manager')
        print('Groups created...Ok')

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

        admin_admin = User(
            username='admin',
            email='admin@admin.com')
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
        )
        guest1.set_password('guest1')
        guest1.save()
        guest1.groups.add(Group.objects.get(name='Guest'))

        guest2 = Guest(
            username='guest2',
            email='guest2@guest2.com',
            first_name='guest2',
        )
        guest2.set_password('guest2')
        guest2.save()
        guest2.groups.add(Group.objects.get(name='Guest'))
        print('Guests created...Ok')

        # ==================================================================================================
        # ==================================================================================================

        chef1 = Chef(
            username='chef1',
            email='chef1@chef1.com',
            first_name='chef1',
        )
        chef1.set_password('chef1')
        chef1.save()
        chef1.groups.add(Group.objects.get(name='Chef'))
        chef1.user_permissions.add(Permission.objects.get(name='Free'))

        chef2 = Chef(
            username='chef2',
            email='chef2@chef2.com',
            first_name='chef2',
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
        )
        monitor1.set_password('monitor1')
        monitor1.save()
        monitor1.groups.add(Group.objects.get(name='Monitor'))
        monitor1.user_permissions.add(Permission.objects.get(name='Free'))

        monitor2 = Monitor(
            username='monitor2',
            email='monitor2@monitor2.com',
            first_name='monitor2',
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
        )
        manager1.set_password('manager1')
        manager1.save()
        manager1.groups.add(Group.objects.get(name='Manager'))
        manager1.user_permissions.add(Permission.objects.get(name='Free'))

        manager2 = Manager(
            username='manager2',
            email='manager1@manager2.com',
            first_name='manager2',
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
            owner=monitor2,
        )
        activity2.save()
        activity2.assistants.add(guest1)

        print ('Activities... ok')
        # ==================================================================================================
        # ==================================================================================================

        local1 = Local(
            name='local1',
            description='description',
            address='address1',
            latitude=10.00,
            longitude=12.00,
            manager=manager1)
        local1.save()

        local2 = Local(
            name='local2',
            description='description',
            address='address2',
            latitude=10.00,
            longitude=12.00,
            manager=manager2)
        local2.save()

        print ('Locals... Ok')

        print('Populating database...OK\n'
              'Ready to use!')

    def handle(self, *args, **options):
        self._migrate()