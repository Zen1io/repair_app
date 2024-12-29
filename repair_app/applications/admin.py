from django.contrib import admin
from .models import (Application,
                     ApplicationComponentItem, ApplicationServiceItem)


class ApplicationComponentItemInline(admin.TabularInline):

    model = ApplicationComponentItem
    raw_id_fields = ['component']


class ApplicationServiceItemInline(admin.TabularInline):

    model = ApplicationServiceItem
    raw_id_fields = ['service']


@admin.register(Application)
class Application(admin.ModelAdmin):

    list_display = ['id', 'first_name', 'last_name', 'email',
                    'category', 'date_of_access', 'date_of_readiness',
                    'comment', 'master', 'get_total_cost']
    inlines = [ApplicationComponentItemInline, ApplicationServiceItemInline]
