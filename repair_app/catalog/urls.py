from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'catalog'

urlpatterns = [
    path('',
         views.CatalogOptionPage.as_view(), name='catalog_option'),
    path('service_list/',
         views.CategoryListView.as_view(), name='service_list'),
    path('service_list/<slug:category_slug>/',
         views.ServiceListView.as_view(), name='services_by_category'),
    path('components/',
         views.ComponentListView.as_view(), name='component_list'),
    path('component_list/<slug:category_slug>/',
         views.ComponentListView.as_view(), name='component_list_by_category'),
    path('components/<int:pk>/',
         views.ComponentDetailView.as_view(), name='component_detail'),
]
