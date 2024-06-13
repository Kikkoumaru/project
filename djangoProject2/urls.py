from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from abaranti import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', views.user_login, name='login'),  # ログインURLを追加
    path('accounts/logout', views.user_logout, name='logout'),
    path('abaranti/', include('abaranti.urls')),
    path('', views.patient_list, name='patient_list'),
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico', permanent=True)),
]
