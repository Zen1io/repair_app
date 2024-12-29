from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'applications'

urlpatterns = [
    path('list/',
         login_required(views.ApplicationListView.as_view()),
         name='applications_list'),
    path('create/',
         login_required(views.ApplicationCreateView.as_view()),
         name='application_create'),
    path('edit/<int:pk>/',
         login_required(views.ApplicationEditView.as_view()),
         name='application_edit'),
    path('delete/<int:pk>/',
         login_required(views.ApplicationDeleteView.as_view()),
         name='application_delete'),
    path('<int:application_id>/pdf',
         views.create_application_pdf, name='application_pdf')
]
