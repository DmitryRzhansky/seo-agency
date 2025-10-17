from django.shortcuts import render, get_object_or_404
from main.models import Post
from django.core.paginator import Paginator
from django.db.models import F


def post_list(request):
	posts_list = Post.objects.filter(is_published=True).order_by('-published_date')
	paginator = Paginator(posts_list, 10)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	return render(request, 'main/post_list.html', {
		'title': 'Блог | Полезные статьи о продвижении',
		'page_obj': page_obj,
		'is_paginated': page_obj.has_other_pages(),
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
