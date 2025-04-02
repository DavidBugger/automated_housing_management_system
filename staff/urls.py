from django.urls import path
from . import views

urlpatterns = [
    path('staff_dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('view_document/', views.document_list, name='view_document'),
    path('approve/<int:document_id>/', views.approve_document, name='approve_document'),
    path('staff_login/', views.staff_login, name='staff_login'),
    path('upload_document/', views.upload_document, name='upload_document'),
]