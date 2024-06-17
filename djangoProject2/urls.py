from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from abaranti import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', views.user_login, name='login'),  # ログインURLを追加
    path('accounts/logout/', views.user_logout, name='logout'),
    path('accounts/register/', views.register, name='register'),  # 登録ページのURL設定
    path('abaranti/', include('abaranti.urls')),
    path('employee_register/', views.employee_register, name='employee_register'),  # 従業員登録URLの追加
    path('', views.patient_list, name='home'),
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico', permanent=True)),
]
