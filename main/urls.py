from django.urls import path
from . import views

app_name = 'main' # Используется для namespace='main' в project_config/urls.py

urlpatterns = [
    # Главная страница (landing page)
    path('', views.index, name='home'),

    # --- Услуги ---
    # Общая страница со списком услуг (если планируется)
    # path('services/', views.service_list, name='service_list'),

    # Страница раздела услуг (например, /services/seo-prodvizhenie/)
    path('services/<slug:slug>/', views.service_category_detail, name='service_category'),

    # Страница отдельной услуги (например, /service/audit-saita/)
    path('service/<slug:slug>/', views.service_detail, name='service_detail'),


    # --- Блог ---
    # Общая страница блога со списком постов
    path('blog/', views.post_list, name='post_list'),

    # Страница отдельного поста (например, /blog/kak-vybrat-seo-agentstvo/)
    path('blog/<slug:slug>/', views.post_detail, name='post_detail'),


    # --- Дополнительные страницы ---
    # path('contacts/', views.contacts, name='contacts'),
    # path('faq/', views.faq, name='faq'),
    # path('privacy/', views.privacy_policy, name='privacy_policy'),

]