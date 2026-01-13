from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_novel, name='upload_novel'),
    
    path('project/<int:project_id>/analyze/start/', views.start_analysis, name='start_analysis'),
    path('project/<int:project_id>/analyze/continue/', views.continue_analysis, name='continue_analysis'),
    path('project/<int:project_id>/analyze/finalize/', views.finalize_analysis, name='finalize_analysis'),
    path('project/<int:project_id>/analyze/progress/', views.get_analysis_progress, name='get_analysis_progress'),
    
    path('project/<int:project_id>/session/start/', views.start_creative_session, name='start_creative_session'),
    path('session/<int:session_id>/chat/', views.creative_chat, name='creative_chat'),
    path('session/<int:session_id>/generate/', views.generate_content, name='generate_content'),
    path('session/<int:session_id>/apply/', views.apply_modification, name='apply_modification'),
    
    path('project/<int:project_id>/custom-content/', views.save_custom_content, name='save_custom_content'),
    path('project/<int:project_id>/custom-content/list/', views.list_custom_content, name='list_custom_content'),
    
    path('project/<int:project_id>/history/', views.get_modification_history, name='get_modification_history'),
    path('project/<int:project_id>/history/<int:log_id>/revert/', views.revert_modification, name='revert_modification'),
]
