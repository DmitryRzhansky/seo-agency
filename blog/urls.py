from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
	path('', views.post_list, name='post_list'),
	path('search/', views.search_posts, name='search'),
	path('category/<slug:category_slug>/<slug:post_slug>/', views.post_detail, name='post_detail'),
	path('category/<slug:slug>/', views.category_posts, name='category_posts'),
	path('<slug:slug>/', views.post_detail_legacy, name='post_detail_legacy'),  # Старый URL для обратной совместимости
]
