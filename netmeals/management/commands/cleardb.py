# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Permission
from django.contrib.auth.models import Group
from activities.models import Local, Activity
from users.models import Guest, Chef, Monitor, Manager


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

    def handle(self, *args, **options):
        self._migrate()
