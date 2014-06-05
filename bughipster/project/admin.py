"""
bughispster.project.admin
~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2013-2014 by Xavier Ordoquy, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""
from django.contrib import admin
from . import models


class ProductAdmin(admin.ModelAdmin):
    pass


class ComponentAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'owner', 'active')


admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Component, ComponentAdmin)
