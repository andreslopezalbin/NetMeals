# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from datetime import date
from django.utils.translation import ugettext_lazy as _

# Stdlib imports

# Core Django imports
from django import template

# Third-party app imports

# Realative imports of the 'app-name' package
from math import modf

register = template.Library()


@register.filter('floatToInt')
def floatToInt(avg):
    return range(int(avg))


@register.filter('redondeo')
def redondeo(avg):
    b, a = modf(avg)
    if b >= 0.5:
        return True
