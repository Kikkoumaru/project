from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/<str:pat_id>/', views.patient_detail, name='patient_detail'),
    path('patients/create/', views.patient_create, name='patient_create'),
    path('patients/<str:pat_id>/update/', views.patient_update, name='patient_update'),
    path('patients/<str:pat_id>/delete/', views.patient_delete, name='patient_delete'),
]
