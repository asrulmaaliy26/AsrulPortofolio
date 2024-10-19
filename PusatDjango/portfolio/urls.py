from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    # Link URLs
    path('links/', views.link_list, name='link_list'),
    path('links/<int:pk>/', views.link_detail, name='link_detail'),
    path('links/create/', views.link_create, name='link_create'),
    path('links/edit/<int:pk>/', views.link_edit, name='link_edit'),

    # Image URLs
    path('images/', views.image_list, name='image_list'),
    path('images/<int:pk>/', views.image_detail, name='image_detail'),
    path('images/create/', views.image_create, name='image_create'),
    path('images/edit/<int:pk>/', views.image_edit, name='image_edit'),

    # Project URLs
    path('projects/', views.project_list, name='project_list'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('projects/create/', views.project_create, name='project_create'),
    path('projects/edit/<int:pk>/', views.project_edit, name='project_edit'),

    # Skill URLs
    path('skills/', views.skill_list, name='skill_list'),
    path('skills/<int:pk>/', views.skill_detail, name='skill_detail'),
    path('skills/create/', views.skill_create, name='skill_create'),
    path('skills/edit/<int:pk>/', views.skill_edit, name='skill_edit'),

    # Experience URLs
    path('experiences/', views.experience_list, name='experience_list'),
    path('experiences/<int:pk>/', views.experience_detail, name='experience_detail'),
    path('experiences/create/', views.experience_create, name='experience_create'),
    path('experiences/edit/<int:pk>/', views.experience_edit, name='experience_edit'),
]
