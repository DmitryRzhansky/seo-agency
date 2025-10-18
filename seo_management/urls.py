from django.urls import path
from . import views

app_name = 'seo_management'

urlpatterns = [
    path('sitemap.xml', views.sitemap_view, name='sitemap'),
    path('robots.txt', views.robots_txt_view, name='robots_txt'),
]
