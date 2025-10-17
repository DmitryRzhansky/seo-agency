from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Count, F
from django.contrib import messages
# from django.core.mail import send_mail # Раскомментировать для отправки реальной почты

# Импорт моделей и формы
from .models import ServiceCategory, Service, Post, ContactRequest, TeamMember, Testimonial
from .forms import ContactForm
from django.views.decorators.cache import never_cache # отключаем кэш для index
from django.conf import settings # <<< Импорт settings для времени кэша

# --- Главная страница (Landing Page) ---
@never_cache
def index(request):
    """
    Главная страница (лендинг). 
    Обрабатывает форму ContactForm, агрегирует данные и передает их в шаблон.
    """
    
    # 1. ОБРАБОТКА ФОРМЫ (POST-запрос)
    if request.method == 'POST':
        form = ContactForm(request.POST) 
        if form.is_valid():
            # Сохраняем заявку в базу данных
            form.save()
            
            # TODO: Здесь можно добавить логику отправки email уведомления
            
            messages.success(request, 'Спасибо! Ваша заявка успешно отправлена. Мы свяжемся с вами в ближайшее время.')
            
            # Редирект на главную страницу
            return redirect('main:home') 
        else:
            # Если форма невалидна, добавляем сообщение об ошибке
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
            # Форма с ошибками будет передана в контекст ниже
    
    # 2. ИНИЦИАЛИЗАЦИЯ ФОРМЫ (GET-запрос)
    else:
        # Если это GET-запрос, создаем пустую форму
        form = ContactForm()
        
    # 3. Получение данных для рендера страницы
    top_services = Service.objects.all().order_by('order')[:6] 
    recent_posts = Post.objects.filter(is_published=True).order_by('-published_date')[:3]
    team_members = TeamMember.objects.filter(is_active=True).order_by('order')
    testimonials = Testimonial.objects.filter(is_active=True).order_by('order')

    # Список городов для секции Locations
    cities_list = [
        "Москва", "Санкт-Петербург", "Новосибирск", "Екатеринбург", 
        "Казань", "Нижний Новгород", "Самара", "Челябинск", 
        "Ростов-на-Дону", "Уфа", "Красноярск", "Пермь", 
        "Воронеж", "Волгоград", "Минск", "Астана", 
        "Алматы", "Киев"
    ]
    
    context = {
        'title': 'Комплексное продвижение бизнеса | Isakov Agency',
        'top_services': top_services,
        'recent_posts': recent_posts,
        'cities_list': cities_list,
        'form': form, # <<< Форма передается в шаблон
        'team_members': team_members,
        'testimonials': testimonials,
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

@never_cache
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


@never_cache
def post_detail(request, slug):
    """
    Страница отдельного поста в блоге.
    """
    post = get_object_or_404(Post, slug=slug)
    
    # Инкремент просмотров один раз на сессию для каждой статьи
    session_key = f"viewed_post_{post.pk}"
    if not request.session.get(session_key):
        Post.objects.filter(pk=post.pk).update(views_count=F('views_count') + 1)
        # Обновляем объект в памяти, чтобы в шаблоне было актуальное значение
        post.refresh_from_db(fields=['views_count'])
        request.session[session_key] = True
    
    # Можно добавить логику для "Похожих постов" или "Следующий/Предыдущий пост"
    
    context = {
        'title': post.title,
        'post': post,
    }
    return render(request, 'main/post_detail.html', context)