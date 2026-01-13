from django.urls import path
from . import views

urlpatterns = [
    path('projects/', views.list_projects, name='list_projects'),
    path('project/<int:project_id>/', views.get_game_data, name='get_game_data'),
    path('project/<int:project_id>/chapter/<str:chapter_id>/', views.get_chapter, name='get_chapter'),
    path('project/<int:project_id>/scene/<str:scene_id>/', views.get_scene, name='get_scene'),
    
    path('project/<int:project_id>/save/', views.save_game, name='save_game'),
    path('project/<int:project_id>/load/<int:slot>/', views.load_game, name='load_game'),
    path('project/<int:project_id>/saves/', views.list_saves, name='list_saves'),
    path('project/<int:project_id>/save/<int:slot>/delete/', views.delete_save, name='delete_save'),
    
    path('project/<int:project_id>/check-condition/', views.check_condition, name='check_condition'),
]
