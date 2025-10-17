from django.shortcuts import render, get_object_or_404
from main.models import Post
from .models import Category
from django.core.paginator import Paginator
from django.db.models import F


def post_list(request):
	posts_list = Post.objects.filter(is_published=True).order_by('-published_date')
	paginator = Paginator(posts_list, 10)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	
	# Получаем все активные категории для фильтрации
	categories = Category.objects.filter(is_active=True).order_by('order', 'name')
	
	return render(request, 'main/post_list.html', {
		'title': 'Блог | Полезные статьи о продвижении',
		'page_obj': page_obj,
		'is_paginated': page_obj.has_other_pages(),
		'categories': categories,
		'current_category': None,
	})


def category_posts(request, slug):
	"""Отображение статей конкретной категории"""
	category = get_object_or_404(Category, slug=slug, is_active=True)
	posts_list = Post.objects.filter(
		is_published=True, 
		category=category
	).order_by('-published_date')
	
	paginator = Paginator(posts_list, 10)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	
	# Получаем все активные категории для фильтрации
	categories = Category.objects.filter(is_active=True).order_by('order', 'name')
	
	return render(request, 'main/post_list.html', {
		'title': f'{category.name} | Блог',
		'page_obj': page_obj,
		'is_paginated': page_obj.has_other_pages(),
		'categories': categories,
		'current_category': category,
	})


def post_detail(request, slug):
	post = get_object_or_404(Post, slug=slug)
	session_key = f"viewed_post_{post.pk}"
	if not request.session.get(session_key):
		Post.objects.filter(pk=post.pk).update(views_count=F('views_count') + 1)
		post.refresh_from_db(fields=['views_count'])
		request.session[session_key] = True
	return render(request, 'main/post_detail.html', {
		'title': post.title,
		'post': post,
	})
