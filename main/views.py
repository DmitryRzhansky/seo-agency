from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Count, F, Q
from django.contrib import messages
from django.urls import reverse
# from django.core.mail import send_mail # Раскомментировать для отправки реальной почты

# Импорт моделей и формы
from .models import City, ServiceCategory, Service, ContactRequest, TeamMember, Testimonial, PortfolioItem, HomePage, FAQCategory, FAQItem
from blog.models import Post, Category
from .forms import ContactForm
from pages.models import SimplePage
from django.views.decorators.cache import never_cache  # cache_page ОТКЛЮЧЕН
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
    
    # Получаем настройки главной страницы
    try:
        home_page = HomePage.objects.filter(is_active=True).first()
        if not home_page:
            # Создаем дефолтную главную страницу, если её нет
            home_page = HomePage.objects.create()
    except:
        home_page = None
    
    context = {
        'title': home_page.hero_title if home_page else 'Комплексное продвижение бизнеса | Isakov Agency',
        'top_services': top_services,
        'recent_posts': recent_posts,
        'cities_list': cities_list,
        'form': form, # <<< Форма передается в шаблон
        'team_members': team_members,
        'testimonials': testimonials,
        'home_page': home_page,
        'seo_object': home_page,
        'page_type': 'home',
        'page_slug': None,
    }
    return render(request, 'main/index_new.html', context)


# --- Представления для Услуг ---

def service_category_detail(request, slug):
    """
    Страница раздела услуг (например, /services/seo-prodvizhenie/).
    Показывает информацию о категории и список всех услуг в ней.
    """
    category = get_object_or_404(ServiceCategory, slug=slug)
    # Получаем все услуги, связанные с этой категорией, отсортированные по порядку
    services_in_category = Service.objects.filter(category=category, is_published=True).order_by('order')
    
    # Добавляем пагинацию
    from django.core.paginator import Paginator
    paginator = Paginator(services_in_category, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title': category.title,
        'category': category,
        'services': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'seo_object': category,  # Передаем категорию как SEO-объект
    }
    return render(request, 'main/service_category.html', context)


def service_detail(request, slug):
    """
    Страница отдельной услуги (например, /service/audit-saita/).
    """
    service = get_object_or_404(Service, slug=slug)
    
    # Получаем связанные услуги
    related_services = service.get_related_services(limit=3)

    context = {
        'title': service.title,
        'service': service,
        'related_services': related_services,
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

# @cache_page(300)  # КЭШИРОВАНИЕ ОТКЛЮЧЕНО
def city_list(request):
    """
    Страница со списком всех городов-миллионников.
    """
    cities = City.objects.filter(is_active=True).order_by('order', 'name')
    
    context = {
        'title': 'Города присутствия | SEO продвижение по России',
        'cities': cities,
        'seo_object': None,
        'page_type': 'city_list',
        'page_slug': None,
    }
    return render(request, 'main/city_list_brutal.html', context)


@never_cache
def city_detail(request, slug):
    """
    Страница отдельного города с региональной информацией.
    """
    city = get_object_or_404(City, slug=slug, is_active=True)
    
    # Получаем услуги и статьи для этого города
    services = Service.objects.filter(is_published=True).select_related('category').order_by('order')
    recent_posts = Post.objects.filter(is_published=True).order_by('-published_date')[:6]
    
    # Получаем категории услуг для фильтрации
    service_categories = ServiceCategory.objects.all().prefetch_related('services')
    
    context = {
        'title': city.get_local_title(),
        'city': city,
        'services': services,
        'service_categories': service_categories,
        'recent_posts': recent_posts,
        'seo_object': city,
        'page_type': 'city_detail',
        'page_slug': city.slug,
    }
    return render(request, 'main/city_detail_brutal.html', context)


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
        'page_type': 'city_service_detail',
        'page_slug': f"{city.slug}/{service.slug}",
    }
    return render(request, 'main/city_service_detail_brutal.html', context)


@never_cache
def city_category_detail(request, city_slug, category_slug):
    """
    Страница категории услуг в конкретном городе.
    """
    city = get_object_or_404(City, slug=city_slug, is_active=True)
    category = get_object_or_404(ServiceCategory, slug=category_slug)
    
    # Получаем услуги этой категории
    services = Service.objects.filter(category=category, is_published=True).order_by('order')
    
    context = {
        'title': f"{category.title} в {city.name}",
        'city': city,
        'category': category,
        'services': services,
        'seo_object': category,
        'page_type': 'city_category_detail',
        'page_slug': f"{city.slug}/{category.slug}",
    }
    return render(request, 'main/city_category_detail_brutal.html', context)


@never_cache
def city_post_detail(request, city_slug, post_slug):
    """
    Страница статьи блога в контексте конкретного города.
    """
    city = get_object_or_404(City, slug=city_slug, is_active=True)
    post = get_object_or_404(Post, slug=post_slug, is_published=True)
    
    # Инкремент просмотров (для базовой статьи)
    session_key = f"viewed_post_{post.pk}"
    if not request.session.get(session_key):
        Post.objects.filter(pk=post.pk).update(views_count=F('views_count') + 1)
        post.refresh_from_db(fields=['views_count'])
        request.session[session_key] = True
    
    # Получаем связанные статьи
    related_posts = post.get_related_posts(limit=3)
    
    # Получаем региональную адаптацию
    from main.models import RegionalPostAdaptation
    try:
        regional_adaptation = RegionalPostAdaptation.objects.get(
            post=post, 
            city=city, 
            is_active=True
        )
        
        # Создаем объект с региональными данными
        class RegionalPost:
            def __init__(self, post, adaptation):
                self.base_post = post
                self.adaptation = adaptation
                
            @property
            def title(self):
                return self.adaptation.get_title()
                
            @property
            def content(self):
                return self.adaptation.get_content()
                
            @property
            def description(self):
                return self.adaptation.get_description()
                
            def __getattr__(self, name):
                return getattr(self.base_post, name)
        
        # Инкремент просмотров для региональной адаптации
        regional_session_key = f"viewed_regional_{regional_adaptation.pk}"
        if not request.session.get(regional_session_key):
            RegionalPostAdaptation.objects.filter(pk=regional_adaptation.pk).update(views_count=F('views_count') + 1)
            regional_adaptation.refresh_from_db(fields=['views_count'])
            request.session[regional_session_key] = True
        
        regional_post = RegionalPost(post, regional_adaptation)
        
    except RegionalPostAdaptation.DoesNotExist:
        # Если нет региональной адаптации, используем базовую статью
        regional_post = post
    
    context = {
        'title': f"{regional_post.title} | {city.name}",
        'city': city,
        'post': regional_post,
        'related_posts': related_posts,
        'seo_object': regional_post,
        'page_type': 'city_post_detail',
        'page_slug': f"{city.slug}/{post.slug}",
    }
    return render(request, 'main/city_post_detail_brutal.html', context)


def set_city(request, slug):
    """
    Устанавливает выбранный город в сессии пользователя
    """
    from .models import City
    
    try:
        city = City.objects.get(slug=slug, is_active=True)
        request.session['user_city'] = slug
        
        # Перенаправляем на страницу выбранного города
        return redirect('main:city_detail', slug=slug)
    except City.DoesNotExist:
        # Если город не найден, перенаправляем на список городов
        return redirect('main:city_list')


def contacts(request):
    """
    Страница контактов с формой обратной связи
    """
    # Обработка формы
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Спасибо! Ваше сообщение отправлено. Мы свяжемся с вами в ближайшее время.')
            return redirect('main:contacts')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = ContactForm()
    
    context = {
        'title': 'Контакты | Isakov Agency',
        'form': form,
        'seo_object': None,  # Можно создать отдельную SEO модель для страницы контактов
    }
    return render(request, 'main/contacts_brutal.html', context)


def privacy_policy(request):
    """
    Страница политики конфиденциальности
    """
    context = {
        'title': 'Политика конфиденциальности | Isakov Agency',
        'seo_object': None,
    }
    return render(request, 'main/privacy_policy_brutal.html', context)


# --- Портфолио ---

# @cache_page(300)  # КЭШИРОВАНИЕ ОТКЛЮЧЕНО
def portfolio_list(request):
    """
    Страница со списком всех работ в портфолио с фильтрацией и поиском
    """
    # Получаем все опубликованные работы (фильтрация теперь происходит на клиенте)
    portfolio_items = PortfolioItem.objects.filter(is_published=True).order_by('order', '-created_at')
    
    # Получаем тип проекта для передачи в шаблон (но не фильтруем на сервере)
    project_type = request.GET.get('type')
    
    # Поиск по названию, описанию и клиенту
    search_query = request.GET.get('q', '').strip()
    if search_query:
        from django.db.models import Q
        portfolio_items = portfolio_items.filter(
            Q(title__icontains=search_query) |
            Q(short_description__icontains=search_query) |
            Q(client_name__icontains=search_query)
        ).distinct()
    
    # Пагинация для всех работ
    paginator = Paginator(portfolio_items, 9)  # 9 работ на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Получаем рекомендуемые проекты для отдельного блока (с пагинацией)
    featured_projects = PortfolioItem.objects.filter(
        is_published=True, 
        is_featured=True
    ).order_by('order', '-created_at')
    
    # Пагинация для рекомендуемых проектов
    featured_paginator = Paginator(featured_projects, 6)  # 6 рекомендуемых проектов на страницу
    featured_page_number = request.GET.get('featured_page', 1)
    featured_page_obj = featured_paginator.get_page(featured_page_number)
    
    # Получаем все типы проектов для фильтрации
    project_types = PortfolioItem.objects.filter(is_published=True).values_list('project_type', flat=True).distinct()
    project_type_choices = [
        ('seo', 'SEO-продвижение'),
        ('context', 'Контекстная реклама'),
        ('smm', 'SMM'),
        ('design', 'Дизайн'),
        ('development', 'Разработка'),
        ('complex', 'Комплексное продвижение'),
    ]
    available_types = [(choice[0], choice[1]) for choice in project_type_choices if choice[0] in project_types]
    
    context = {
        'title': 'Портфолио | Isakov Agency',
        'page_obj': page_obj,
        'featured_page_obj': featured_page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'is_featured_paginated': featured_page_obj.has_other_pages(),
        'available_types': available_types,
        'current_type': project_type,
        'search_query': search_query,
        'seo_object': None,  # Можно создать отдельную SEO модель для страницы портфолио
        'page_type': 'portfolio_list',
        'page_slug': None,
    }
    return render(request, 'main/portfolio_list_brutal.html', context)


def portfolio_detail(request, slug):
    """
    Детальная страница работы из портфолио
    """
    portfolio_item = get_object_or_404(PortfolioItem, slug=slug, is_published=True)
    
    # Получаем похожие проекты (из той же категории или последние)
    related_projects = PortfolioItem.objects.filter(
        is_published=True
    ).exclude(pk=portfolio_item.pk).order_by('order', '-created_at')[:3]
    
    context = {
        'title': f'{portfolio_item.title} | Портфолио | Isakov Agency',
        'portfolio_item': portfolio_item,
        'related_projects': related_projects,
        'seo_object': portfolio_item,
        'page_type': 'portfolio_detail',
        'page_slug': portfolio_item.slug,
    }
    return render(request, 'main/portfolio_detail_brutal.html', context)


def sitemap_page(request):
    """
    HTML-страница карты сайта с красивым дизайном
    """
    # Получаем все данные для карты сайта
    service_categories = ServiceCategory.objects.all().prefetch_related('services')
    all_services = Service.objects.filter(is_published=True)  # Все услуги для подсчета
    blog_categories = Category.objects.all().prefetch_related('post_set')
    blog_posts = Post.objects.filter(is_published=True).select_related('category')
    cities = City.objects.all()
    pages = SimplePage.objects.filter(is_published=True)
    
    # Создаем структуру карты сайта
    sitemap_data = {
        'main_pages': [
            {'title': 'Главная', 'url': '/', 'description': 'Главная страница агентства'},
            {'title': 'Услуги', 'url': '/services/', 'description': 'Все наши услуги'},
            {'title': 'Блог', 'url': '/blog/', 'description': 'Статьи и новости'},
            {'title': 'Портфолио', 'url': '/portfolio/', 'description': 'Примеры наших работ'},
            {'title': 'Контакты', 'url': '/#contact', 'description': 'Свяжитесь с нами'},
        ],
        'services': service_categories,
        'all_services': all_services,  # Добавляем все услуги для подсчета
        'blog_categories': blog_categories,
        'blog_posts': blog_posts,
        'cities': cities,
        'pages': pages,
    }
    
    context = {
        'title': 'Карта сайта | Isakov Agency',
        'sitemap_data': sitemap_data,
        'page_type': 'sitemap',
    }
    return render(request, 'main/sitemap_brutal.html', context)


# --- FAQ (Вопрос-Ответ) ---

@never_cache
def faq_list(request):
    """
    Список всех FAQ с фильтрацией по категориям и поиском
    """
    # Получаем все активные категории
    categories = FAQCategory.objects.filter(is_active=True).order_by('order', 'name')
    
    # Фильтрация по категории
    category_slug = request.GET.get('category')
    selected_category = None
    faq_by_category = {}
    search_query = request.GET.get('search', '').strip()
    
    if category_slug:
        try:
            selected_category = FAQCategory.objects.get(slug=category_slug, is_active=True)
            # Получаем вопросы только для выбранной категории
            faq_items = FAQItem.objects.filter(
                category=selected_category,
                is_published=True
            ).order_by('order', 'question')
            
            # Поиск по вопросам и ответам
            if search_query:
                faq_items = faq_items.filter(
                    Q(question__icontains=search_query) | 
                    Q(answer__icontains=search_query)
                )
            
            # Группируем вопросы по категориям
            for item in faq_items:
                category = item.category
                if category not in faq_by_category:
                    faq_by_category[category] = []
                faq_by_category[category].append(item)
        except FAQCategory.DoesNotExist:
            selected_category = None
    
    # SEO данные
    seo_title = "Часто задаваемые вопросы | Isakov Agency"
    seo_description = "Ответы на популярные вопросы о SEO-продвижении, контекстной рекламе и digital-маркетинге. Найдем ответ на ваш вопрос!"
    seo_keywords = "FAQ, вопросы, ответы, SEO, продвижение, контекстная реклама"
    
    # Создаем простой объект для хлебных крошек
    class FAQPage:
        def get_breadcrumbs(self):
            return [
                {"title": "Главная", "url": "/"},
                {"title": "FAQ", "url": "/faq/"}
            ]
    
    faq_page = FAQPage()
    
    context = {
        'title': seo_title,
        'seo_description': seo_description,
        'seo_keywords': seo_keywords,
        'categories': categories,
        'faq_by_category': faq_by_category,
        'selected_category': selected_category,
        'search_query': search_query,
        'page_type': 'faq_list',
        'faq_page': faq_page,  # Объект для хлебных крошек
    }
    
    return render(request, 'main/faq_brutal.html', context)


@never_cache
def faq_category(request, slug):
    """
    FAQ по конкретной категории
    """
    category = get_object_or_404(FAQCategory, slug=slug, is_active=True)
    
    # Получаем все опубликованные вопросы этой категории
    faq_items = FAQItem.objects.filter(
        category=category,
        is_published=True
    ).order_by('order', 'question')
    
    # Поиск по вопросам и ответам
    search_query = request.GET.get('search', '').strip()
    if search_query:
        faq_items = faq_items.filter(
            Q(question__icontains=search_query) | 
            Q(answer__icontains=search_query)
        )
    
    # SEO данные
    seo_title = f"{category.name} - Часто задаваемые вопросы | Isakov Agency"
    seo_description = category.description or f"Ответы на вопросы по теме: {category.name}"
    seo_keywords = f"FAQ, {category.name}, вопросы, ответы"
    
    context = {
        'title': seo_title,
        'seo_description': seo_description,
        'seo_keywords': seo_keywords,
        'category': category,
        'faq_items': faq_items,
        'search_query': search_query,
        'page_type': 'faq_category',
    }
    
    return render(request, 'main/faq_category_brutal.html', context)


@never_cache
def faq_item(request, category_slug, item_id):
    """
    Отдельный вопрос-ответ
    """
    category = get_object_or_404(FAQCategory, slug=category_slug, is_active=True)
    faq_item = get_object_or_404(FAQItem, id=item_id, category=category, is_published=True)
    
    
    # Получаем похожие вопросы из той же категории
    related_items = FAQItem.objects.filter(
        category=category,
        is_published=True
    ).exclude(id=faq_item.id).order_by('order', 'question')[:5]
    
    # SEO данные
    seo_title = f"{faq_item.question} | FAQ | Isakov Agency"
    seo_description = f"Ответ на вопрос: {faq_item.question}"
    seo_keywords = f"FAQ, {category.name}, {faq_item.question}"
    
    context = {
        'title': seo_title,
        'seo_description': seo_description,
        'seo_keywords': seo_keywords,
        'category': category,
        'faq_item': faq_item,
        'related_items': related_items,
        'page_type': 'faq_item',
    }
    
    return render(request, 'main/faq_item_brutal.html', context)