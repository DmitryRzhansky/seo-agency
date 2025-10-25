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
    path('cities/<slug:city_slug>/category/<slug:category_slug>/', views.city_category_detail, name='city_category_detail'),
    path('cities/<slug:city_slug>/blog/<slug:post_slug>/', views.city_post_detail, name='city_post_detail'),
    path('set-city/<slug:slug>/', views.set_city, name='set_city'),
    
    # --- Дополнительные страницы ---
    path('contacts/', views.contacts, name='contacts'),
    path('privacy/', views.privacy_policy, name='privacy_policy'),
    
    # --- Портфолио ---
    path('portfolio/', views.portfolio_list, name='portfolio_list'),
    path('portfolio/<slug:slug>/', views.portfolio_detail, name='portfolio_detail'),
    
    # --- Карта сайта ---
    path('sitemap/', views.sitemap_page, name='sitemap'),
    
    # --- FAQ (Вопрос-Ответ) ---
    path('faq/', views.faq_list, name='faq_list'),
    path('faq/category/<slug:slug>/', views.faq_category, name='faq_category'),
    path('faq/category/<slug:category_slug>/<slug:item_slug>/', views.faq_item, name='faq_item'),
    
    # --- Глоссарий ---
    path('glossary/', views.glossary_list, name='glossary_list'),
    path('glossary/category/<slug:slug>/', views.glossary_category, name='glossary_category'),
    path('glossary/category/<slug:category_slug>/<slug:term_slug>/', views.glossary_term, name='glossary_term'),

]