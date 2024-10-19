from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_pdf, name='upload_pdf'),
    path('questions/<int:pdf_id>/', views.display_questions_view, name='display_questions'),
    path('results/<int:pdf_id>/', views.show_results_view, name='show_results'),
]
