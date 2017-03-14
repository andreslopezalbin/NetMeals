# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Permission
from activities.models import Guest, Chef, Monitor, Manager


# Los archivos que se encuentren en el paquete commands, se podr�n llamar
# desde manage.py, de forma que para popular la base de datos debemos hacer
# 'manage.py populate_db'

class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def _migrate(self):
        # Drop all tables
        print('Dropping tables...')

        User.objects.all().delete()

        print('Dropping tables...OK')
        print('Populating database...')

        admin_admin = User(
            username='admin',
            email='admin@admin.com')
        admin_admin.set_password('admin')
        admin_admin.is_staff = True
        admin_admin.is_superuser = True
        admin_admin.save()
        # admin_admin.user_permissions.remove(Permission.objects.get(codename="guest"))

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
        guest1.user_permissions.add(Permission.objects.get(codename="guest"))
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
        chef1.user_permissions.add(Permission.objects.get(codename="chef"))
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
        monitor1.user_permissions.add(Permission.objects.get(codename="monitor"))
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
        manager1.user_permissions.add(Permission.objects.get(codename="manager"))
        print('Managers created...Ok')
        print('Assesment...OK\n'
              'Populating database...OK\n'
              'Ready to use!')

        # ==================================================================================================
        # ==================================================================================================

    def handle(self, *args, **options):
        self._migrate()
