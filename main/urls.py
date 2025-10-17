from django.urls import path
from . import views

app_name = 'main' # Используется для namespace='main' в project_config/urls.py

urlpatterns = [
    # Главная страница (landing page)
    path('', views.index, name='home'),
    # остальное перенесено в приложения blog и services


    # --- Дополнительные страницы ---
    # path('contacts/', views.contacts, name='contacts'),
    # path('faq/', views.faq, name='faq'),
    # path('privacy/', views.privacy_policy, name='privacy_policy'),

]