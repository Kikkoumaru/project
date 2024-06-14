from django.urls import path
from . import views

urlpatterns = [
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/create/', views.patient_create, name='patient_create'),
    path('patients/<str:patient_id>/', views.patient_detail, name='patient_detail'),
    path('patients/<str:patient_id>/edit/', views.patient_update, name='patient_update'),
    path('patients/<str:patient_id>/delete/', views.patient_delete, name='patient_delete'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),  # ユーザー登録URLの追加
]
