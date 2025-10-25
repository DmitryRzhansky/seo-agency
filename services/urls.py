from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
	path('', views.service_list, name='service_list'),
	path('category/<slug:category_slug>/<slug:service_slug>/', views.service_detail, name='service_detail'),
	path('category/<slug:slug>/', views.service_category_detail, name='service_category'),
	path('<slug:slug>/', views.service_detail_legacy, name='service_detail_legacy'),  # Старый URL для обратной совместимости
]
