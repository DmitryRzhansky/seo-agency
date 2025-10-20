from django.shortcuts import render, get_object_or_404
from .models import Post
from .models import Category
from django.core.paginator import Paginator
from django.db.models import F, Q
from django.views.decorators.cache import never_cache, cache_page


@cache_page(300)  # 5 минут кэш для списка статей
def post_list(request):
	posts_list = Post.objects.filter(is_published=True).order_by('-published_date')
	paginator = Paginator(posts_list, 9)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	
	# Получаем все активные категории для фильтрации
	categories = Category.objects.filter(is_active=True).order_by('order', 'name')
	
	return render(request, 'main/post_list.html', {
		'title': 'Блог',
		'page_obj': page_obj,
		'is_paginated': page_obj.has_other_pages(),
		'categories': categories,
		'current_category': None,
		'seo_object': None,  # Для списка статей SEO-объект не нужен
	})


@cache_page(300)  # 5 минут кэш для статей категории
def category_posts(request, slug):
	"""Отображение статей конкретной категории"""
	category = get_object_or_404(Category, slug=slug, is_active=True)
	posts_list = Post.objects.filter(
		is_published=True, 
		category=category
	).order_by('-published_date')
	
	paginator = Paginator(posts_list, 9)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	
	# Получаем все активные категории для фильтрации
	categories = Category.objects.filter(is_active=True).order_by('order', 'name')
	
	return render(request, 'main/post_list.html', {
		'title': category.name,
		'page_obj': page_obj,
		'is_paginated': page_obj.has_other_pages(),
		'categories': categories,
		'current_category': category,
		'seo_object': category,  # Передаем категорию как SEO-объект
	})


@never_cache
def search_posts(request):
	"""Поиск по статьям блога"""
	query = request.GET.get('q', '').strip()
	posts_list = Post.objects.filter(is_published=True)
	
	if query:
		# Поиск по заголовку, содержимому и названию категории
		posts_list = posts_list.filter(
			Q(title__icontains=query) |
			Q(content__icontains=query) |
			Q(category__name__icontains=query)
		).distinct()
	
	posts_list = posts_list.order_by('-published_date')
	
	paginator = Paginator(posts_list, 9)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	
	# Получаем все активные категории для фильтрации
	categories = Category.objects.filter(is_active=True).order_by('order', 'name')
	
	title = f'Поиск: "{query}"' if query else 'Поиск по блогу'
	
	return render(request, 'main/post_list.html', {
		'title': title,
		'page_obj': page_obj,
		'is_paginated': page_obj.has_other_pages(),
		'categories': categories,
		'current_category': None,
		'search_query': query,
		'seo_object': None,  # Для поиска SEO-объект не нужен
	})


@never_cache
def post_detail(request, slug):
	post = get_object_or_404(Post, slug=slug)
	session_key = f"viewed_post_{post.pk}"
	if not request.session.get(session_key):
		Post.objects.filter(pk=post.pk).update(views_count=F('views_count') + 1)
		post.refresh_from_db(fields=['views_count'])
		request.session[session_key] = True
	# Получаем связанные статьи для блока "Вам может понравиться"
	related_posts = post.get_related_posts(limit=3)
	
	return render(request, 'main/post_detail.html', {
		'title': post.title,
		'post': post,
		'seo_object': post,  # Передаем пост как SEO-объект
		'related_posts': related_posts,  # Связанные статьи
	})
