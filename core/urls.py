from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('reports/', views.reports, name='reports'),
    path('settings/', views.settings_list, name='settings_list'),
    path('settings/add/', views.settings_create, name='settings_create'),
    path('settings/configurations/', views.config_list, name='config_list'),
    path('settings/configurations/add/', views.config_create, name='config_create'),
    path('settings/configurations/<int:pk>/', views.config_detail, name='config_detail'),
    path('settings/configurations/<int:pk>/edit/', views.config_update, name='config_update'),
    path('settings/configurations/<int:pk>/deactivate/', views.config_deactivate, name='config_deactivate'),
    path('settings/<int:pk>/', views.settings_detail, name='settings_detail'),
    path('settings/<int:pk>/edit/', views.settings_update, name='settings_update'),
    path('settings/<int:pk>/deactivate/', views.settings_deactivate, name='settings_deactivate'),
]
