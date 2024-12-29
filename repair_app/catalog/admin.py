from django.contrib import admin
from .models import Category, Manufacturer, Service, Component


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """."""

    fields = ['title']
    list_display = ['title', 'slug']


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    """."""

    fields = ['title']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """."""

    list_display = ['name', 'price', 'duration']


@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    """."""

    pass
