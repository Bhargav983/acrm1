from django.urls import path

from . import views

app_name = 'consultations'

urlpatterns = [
    path('', views.consultation_list, name='consultation_list'),
    path('add/', views.consultation_create, name='consultation_create'),
    path('<int:pk>/', views.consultation_detail, name='consultation_detail'),
    path('<int:pk>/edit/', views.consultation_update, name='consultation_update'),
    path('<int:pk>/deactivate/', views.consultation_deactivate, name='consultation_deactivate'),
]
