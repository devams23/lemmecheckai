from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_pdf, name='upload_pdf'),
    path('questions/', views.display_questions_view, name='display_questions'),
    path('results/', views.show_results_view, name='show_results'),
] 
