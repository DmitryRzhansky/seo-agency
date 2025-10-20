from django.shortcuts import render, get_object_or_404
from main.models import ServiceCategory, Service


def service_list(request):
	categories = ServiceCategory.objects.all().order_by('order')
	services = Service.objects.all().order_by('order')
	return render(request, 'main/service_list.html', {
		'title': 'Услуги',
		'categories': categories,
		'services': services,
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
