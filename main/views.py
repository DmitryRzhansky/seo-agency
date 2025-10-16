from django.shortcuts import render, get_object_or_404
from .models import ServiceCategory, Service, Post
from django.core.paginator import Paginator
from django.db.models import Count # Будет полезно для отображения кол-ва постов в категориях


# --- Главная страница (Landing Page) ---

def index(request):
    """
    Главная страница (лендинг). 
    Здесь агрегируются данные из разных моделей для отображения.
    """
    # 1. Топ-услуги для секции 'Топ услуг маркетинга'
    # Выбираем услуги, которые мы хотим показать на главной, например, первые 6 по порядку
    top_services = Service.objects.all().order_by('order')[:6] 

    # 2. Недавние посты для секции 'Блог' на главной
    recent_posts = Post.objects.filter(is_published=True).order_by('-published_date')[:3]

    # Для демонстрации можем передать в контекст и другие данные, 
    # если они понадобятся на главной (например, отзывы, команда)
    
    context = {
        'title': 'Комплексное продвижение бизнеса | Isakov Agency',
        'top_services': top_services,
        'recent_posts': recent_posts,
        # Данные для хедера и футера (ServiceCategory) будут добавлены Контекстным процессором
    }
    return render(request, 'main/index.html', context)


# --- Представления для Услуг ---

def service_category_detail(request, slug):
    """
    Страница раздела услуг (например, /services/seo-prodvizhenie/).
    Показывает информацию о категории и список всех услуг в ней.
    """
    category = get_object_or_404(ServiceCategory, slug=slug)
    # Получаем все услуги, связанные с этой категорией, отсортированные по порядку
    services_in_category = Service.objects.filter(category=category).order_by('order')

    context = {
        'title': category.title,
        'category': category,
        'services': services_in_category,
    }
    return render(request, 'main/service_category.html', context)


def service_detail(request, slug):
    """
    Страница отдельной услуги (например, /service/audit-saita/).
    """
    service = get_object_or_404(Service, slug=slug)

    context = {
        'title': service.title,
        'service': service,
    }
    return render(request, 'main/service_detail.html', context)


# --- Представления для Блога ---

def post_list(request):
    """
    Общая страница блога со списком всех постов и пагинацией.
    """
    posts_list = Post.objects.filter(is_published=True).order_by('-published_date')

    # Настройка пагинации: 10 постов на странице
    paginator = Paginator(posts_list, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Список категорий услуг (можно использовать для sidebar блога)
    # categories_with_count = ServiceCategory.objects.annotate(post_count=Count('services'))

    context = {
        'title': 'Блог | Полезные статьи о продвижении',
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        # 'categories_with_count': categories_with_count,
    }
    return render(request, 'main/post_list.html', context)


def post_detail(request, slug):
    """
    Страница отдельного поста в блоге.
    """
    post = get_object_or_404(Post, slug=slug)
    
    # Можно добавить логику для "Похожих постов" или "Следующий/Предыдущий пост"
    
    context = {
        'title': post.title,
        'post': post,
    }
    return render(request, 'main/post_detail.html', context)