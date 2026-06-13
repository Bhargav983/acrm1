from django.urls import path

from . import views

app_name = 'knowledge'

urlpatterns = [
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.category_create, name='category_create'),
    path('categories/<int:pk>/', views.category_detail, name='category_detail'),
    path('categories/<int:pk>/edit/', views.category_update, name='category_update'),
    path('categories/<int:pk>/deactivate/', views.category_deactivate, name='category_deactivate'),
    path('', views.knowledge_list, name='knowledge_list'),
    path('add/', views.knowledge_create, name='knowledge_create'),
    path('<int:pk>/', views.knowledge_detail, name='knowledge_detail'),
    path('<int:pk>/edit/', views.knowledge_update, name='knowledge_update'),
    path('<int:pk>/deactivate/', views.knowledge_deactivate, name='knowledge_deactivate'),
    path('<int:hypothesis_pk>/questions/add/', views.hypothesis_question_create, name='hypothesis_question_create'),
    path('questions/<int:pk>/edit/', views.hypothesis_question_update, name='hypothesis_question_update'),
    path('questions/<int:pk>/deactivate/', views.hypothesis_question_deactivate, name='hypothesis_question_deactivate'),
    path('research-interview/customer/<int:customer_pk>/', views.research_interview_select, name='research_interview_select'),
    path('research-interview/customer/<int:customer_pk>/hypothesis/<int:hypothesis_pk>/', views.research_interview, name='research_interview'),
    path('tracking/', views.tracking_list, name='tracking_list'),
    path('tracking/add/', views.tracking_create, name='tracking_create'),
    path('tracking/<int:pk>/', views.tracking_detail, name='tracking_detail'),
    path('tracking/<int:pk>/edit/', views.tracking_update, name='tracking_update'),
    path('tracking/<int:pk>/deactivate/', views.tracking_deactivate, name='tracking_deactivate'),
]
