from django.urls import path
from . import views

app_name = 'main' # Используется для namespace='main' в project_config/urls.py

urlpatterns = [
    # Главная страница (landing page)
    path('', views.index, name='home'),
    
    # --- Региональные страницы ---
    path('cities/', views.city_list, name='city_list'),
    path('cities/<slug:slug>/', views.city_detail, name='city_detail'),
    path('cities/<slug:city_slug>/services/<slug:service_slug>/', views.city_service_detail, name='city_service_detail'),
    path('cities/<slug:city_slug>/blog/<slug:post_slug>/', views.city_post_detail, name='city_post_detail'),
    
    # --- Дополнительные страницы ---
    # path('contacts/', views.contacts, name='contacts'),
    # path('faq/', views.faq, name='faq'),
    # path('privacy/', views.privacy_policy, name='privacy_policy'),

]