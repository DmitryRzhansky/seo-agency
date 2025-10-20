from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from main.models import ServiceCategory, Service


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

    return render(request, 'main/service_list.html', {
        'title': 'Услуги',
        'categories': categories,
        'services': None,  # не используем общий список напрямую в шаблоне
        'filtered_services': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'current_category': current_category,
        'search_query': query,
        # Для списка услуг SEO-объект не задаем, используем дефолтные мета
    })


def service_category_detail(request, slug):
	category = get_object_or_404(ServiceCategory, slug=slug)
	services_in_category = Service.objects.filter(category=category).order_by('order')
	return render(request, 'main/service_category.html', {
		'title': category.title,
		'category': category,
		'services': services_in_category,
		'seo_object': category,  # Включаем SEO теги категории
	})


def service_detail(request, slug):
	service = get_object_or_404(Service, slug=slug)
	# Получаем связанные услуги для блока "Еще услуги"
	related_services = service.get_related_services(limit=3)
	
	return render(request, 'main/service_detail.html', {
		'title': service.title,
		'service': service,
		'related_services': related_services,  # Связанные услуги
		'seo_object': service,  # Включаем SEO теги услуги
	})
