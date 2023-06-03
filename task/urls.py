from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('tasks/', views.tasks, name='tasks'),
    path('logout/', views.cerrarsesion, name='logout'),
    path('login/', views.login_view, name='login'),
    path('tasks/create/', views.create_task, name='create_task'),
    path('tasks/completed/', views.completed_tasks, name='completed_tasks'),
    path('tasks/<int:task_id>/',views.task_detail, name='task_detail'),
    path('tasks/<int:task_id>/complete',views.complete_task, name='complete_task'),
    path('tasks/delete/<int:task_id>',views.delete_task, name='delete_task'),
    ]