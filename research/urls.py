from django.urls import path
from . import views

urlpatterns = [
    # Project endpoints
    path('projects/<uuid:project_id>/dashboard/', views.get_project_dashboard, name='project-dashboard'),
    
    # Dataset endpoints
    path('datasets/upload/', views.process_uploaded_file, name='dataset-upload'),
    path('datasets/<uuid:dataset_id>/download/', views.download_dataset, name='dataset-download'),
    path('datasets/<uuid:dataset_id>/statistics/', views.get_dataset_statistics, name='dataset-statistics'),
    path('datasets/search/', views.search_datasets, name='dataset-search'),
    
    # External sync
    path('sync/external/<str:external_id>/', views.sync_external_research_data, name='sync-external'),
]