from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Task CRUD
    path('create/', views.create_task, name='create_task'),
    path('update/<int:pk>/', views.update_task, name='update_task'),
    path('delete/<int:pk>/', views.delete_task, name='delete_task'),

    # Quick Productivity Actions
    path('toggle/<int:pk>/', views.toggle_status, name='toggle_status'),
    path('duplicate/<int:pk>/', views.duplicate_task, name='duplicate_task'),

    # Timer Controls
    path('start/<int:pk>/', views.start_timer, name='start_timer'),
    path('pause/<int:pk>/', views.pause_timer, name='pause_timer'),
    path('resume/<int:pk>/', views.resume_timer, name='resume_timer'),
    path('stop/<int:pk>/', views.stop_timer, name='stop_timer'),
]