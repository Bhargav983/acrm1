from django.urls import path

from . import views

app_name = 'customers'

urlpatterns = [
    path('', views.customer_list, name='customer_list'),
    path('api-data/', views.api_data_list, name='api_data_list'),
    path('api-data/add/', views.api_data_create, name='api_data_create'),
    path('api-data/<int:pk>/', views.api_data_detail, name='api_data_detail'),
    path('api-data/<int:pk>/edit/', views.api_data_update, name='api_data_update'),
    path('api-data/<int:pk>/deactivate/', views.api_data_deactivate, name='api_data_deactivate'),
    path('add/', views.customer_create, name='customer_create'),
    path('<int:pk>/', views.customer_detail, name='customer_detail'),
    path('<int:pk>/edit/', views.customer_update, name='customer_update'),
    path('<int:pk>/deactivate/', views.customer_deactivate, name='customer_deactivate'),
]
