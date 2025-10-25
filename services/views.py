from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
# from django.views.decorators.cache import cache_page  # ОТКЛЮЧЕНО
from main.models import ServiceCategory, Service


# @cache_page(300)  # КЭШИРОВАНИЕ ОТКЛЮЧЕНО
def service_list(request):
    categories = ServiceCategory.objects.all().order_by('order')

    # Параметры фильтрации
    query = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category', '').strip()

    current_category = None
    filtered_services = Service.objects.filter(is_published=True).order_by('order')

    if category_slug:
        try:
            current_category = ServiceCategory.objects.get(slug=category_slug)
            filtered_services = filtered_services.filter(category=current_category)
        except ServiceCategory.DoesNotExist:
            current_category = None

    if query:
        filtered_services = filtered_services.filter(
            Q(title__icontains=query) | Q(short_description__icontains=query)
        )

    # Пагинация, как в блоге
    paginator = Paginator(filtered_services, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Выбираем шаблон в зависимости от параметра
    template_name = 'main/service_list_brutal.html'  # Используем брутальный дизайн
    
    return render(request, template_name, {
        'title': 'Услуги',
        'categories': categories,
        'services': None,  # не используем общий список напрямую в шаблоне
        'filtered_services': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'current_category': current_category,
        'category': current_category,  # Добавляем для совместимости с шаблонами
        'search_query': query,
        # Для списка услуг SEO-объект не задаем, используем дефолтные мета
    })


def service_category_detail(request, slug):
	category = get_object_or_404(ServiceCategory, slug=slug)
	services_in_category = Service.objects.filter(category=category, is_published=True).order_by('order')
	
	# Добавляем пагинацию
	from django.core.paginator import Paginator
	paginator = Paginator(services_in_category, 9)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	
	return render(request, 'main/service_category.html', {
		'title': category.title,
		'category': category,
		'services': page_obj,
		'is_paginated': page_obj.has_other_pages(),
		'seo_object': category,  # Включаем SEO теги категории
	})


def service_detail(request, category_slug, service_slug):
	# Получаем категорию для проверки
	category = get_object_or_404(ServiceCategory, slug=category_slug)
	# Получаем услугу по slug и проверяем, что она относится к указанной категории
	service = get_object_or_404(Service, slug=service_slug, category=category)
	# Получаем связанные услуги для блока "Еще услуги"
	related_services = service.get_related_services(limit=3)
	
	return render(request, 'main/service_detail.html', {
		'title': service.title,
		'service': service,
		'category': category,  # Добавляем категорию в контекст
		'related_services': related_services,  # Связанные услуги
		'seo_object': service,  # Включаем SEO теги услуги
	})


def service_detail_legacy(request, slug):
	"""Старый URL для обратной совместимости - делает редирект на новый URL"""
	from django.shortcuts import redirect
	from django.http import Http404
	
	service = get_object_or_404(Service, slug=slug)
	# Делаем редирект на новый URL с указанием категории
	return redirect('services:service_detail', 
	                category_slug=service.category.slug, 
	                service_slug=service.slug, 
	                permanent=True)
