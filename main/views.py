from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Count, F
from django.contrib import messages
# from django.core.mail import send_mail # Раскомментировать для отправки реальной почты

# Импорт моделей и формы
from .models import City, ServiceCategory, Service, Post, ContactRequest, TeamMember, Testimonial
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

    # Получаем активные города из базы данных
    cities_list = City.objects.filter(is_active=True).order_by('order', 'name')
    
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
        'seo_object': category,  # Передаем категорию как SEO-объект
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
        'seo_object': service,  # Передаем услугу как SEO-объект
    }
    return render(request, 'main/service_detail.html', context)


# --- Представления для Блога ---

@never_cache
def post_list(request):
    """
    Общая страница блога со списком всех постов и пагинацией.
    """
    posts_list = Post.objects.filter(is_published=True).order_by('-published_date')

    # Настройка пагинации: 9 постов на странице
    paginator = Paginator(posts_list, 9) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Список категорий услуг (можно использовать для sidebar блога)
    # categories_with_count = ServiceCategory.objects.annotate(post_count=Count('services'))

    context = {
        'title': 'Блог | Полезные статьи о продвижении',
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'seo_object': None,  # Для списка статей SEO-объект не нужен
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
        'seo_object': post,  # Передаем пост как SEO-объект
    }
    return render(request, 'main/post_detail.html', context)


# --- Представления для Городов ---

@never_cache
def city_list(request):
    """
    Страница со списком всех городов-миллионников.
    """
    cities = City.objects.filter(is_active=True).order_by('order', 'name')
    
    context = {
        'title': 'Города присутствия | SEO продвижение по России',
        'cities': cities,
        'seo_object': None,
    }
    return render(request, 'main/city_list.html', context)


@never_cache
def city_detail(request, slug):
    """
    Страница отдельного города с региональной информацией.
    """
    city = get_object_or_404(City, slug=slug, is_active=True)
    
    # Получаем услуги и статьи для этого города
    services = Service.objects.filter(is_published=True).order_by('order')[:6]
    recent_posts = Post.objects.filter(is_published=True).order_by('-published_date')[:3]
    
    context = {
        'title': city.get_local_title(),
        'city': city,
        'services': services,
        'recent_posts': recent_posts,
        'seo_object': city,
    }
    return render(request, 'main/city_detail.html', context)


@never_cache
def city_service_detail(request, city_slug, service_slug):
    """
    Страница услуги в конкретном городе.
    """
    city = get_object_or_404(City, slug=city_slug, is_active=True)
    service = get_object_or_404(Service, slug=service_slug, is_published=True)
    
    # Получаем связанные услуги
    related_services = service.get_related_services(limit=3)
    
    context = {
        'title': f"{service.title} в {city.name}",
        'city': city,
        'service': service,
        'related_services': related_services,
        'seo_object': service,
    }
    return render(request, 'main/city_service_detail.html', context)


@never_cache
def city_post_detail(request, city_slug, post_slug):
    """
    Страница статьи блога в контексте конкретного города.
    """
    city = get_object_or_404(City, slug=city_slug, is_active=True)
    post = get_object_or_404(Post, slug=post_slug, is_published=True)
    
    # Инкремент просмотров
    session_key = f"viewed_post_{post.pk}"
    if not request.session.get(session_key):
        Post.objects.filter(pk=post.pk).update(views_count=F('views_count') + 1)
        post.refresh_from_db(fields=['views_count'])
        request.session[session_key] = True
    
    # Получаем связанные статьи
    related_posts = post.get_related_posts(limit=3)
    
    context = {
        'title': f"{post.title} | {city.name}",
        'city': city,
        'post': post,
        'related_posts': related_posts,
        'seo_object': post,
    }
    return render(request, 'main/city_post_detail.html', context)


def set_city(request, slug):
    """
    Устанавливает выбранный город в сессии пользователя
    """
    from .models import City
    
    try:
        city = City.objects.get(slug=slug, is_active=True)
        request.session['user_city'] = slug
        
        # Перенаправляем на главную страницу
        return redirect('main:home')
    except City.DoesNotExist:
        # Если город не найден, перенаправляем на список городов
        return redirect('main:city_list')