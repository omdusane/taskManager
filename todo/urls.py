from django.urls import path
from .views import home, register, login, logout, dashboard, createTask, viewTasks, updateTask, deleteTask
urlpatterns = [
    
    path('', home, name=''),
    
    path('register', register, name='register'),
    path('login', login, name='login'),    
    path('logout', logout, name='logout'),
    path('dashboard', dashboard, name='dashboard'),
    path('create-task', createTask, name='create-task'),
    path('create-task', createTask, name='create-task'),
    path('view-tasks', viewTasks, name='view-tasks'),
    path('update-task/<str:pk>', updateTask, name='update-task'),
    path('delete-task/<str:pk>', deleteTask, name='delete-task'),


]