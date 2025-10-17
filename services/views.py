from django.shortcuts import render, get_object_or_404
from main.models import ServiceCategory, Service


def service_list(request):
	categories = ServiceCategory.objects.all().order_by('order')
	services = Service.objects.all().order_by('order')
	return render(request, 'main/service_list.html', {
		'title': 'Услуги',
		'categories': categories,
		'services': services,
	})


def service_category_detail(request, slug):
	category = get_object_or_404(ServiceCategory, slug=slug)
	services_in_category = Service.objects.filter(category=category).order_by('order')
	return render(request, 'main/service_category.html', {
		'title': category.title,
		'category': category,
		'services': services_in_category,
	})


def service_detail(request, slug):
	service = get_object_or_404(Service, slug=slug)
	return render(request, 'main/service_detail.html', {
		'title': service.title,
		'service': service,
	})
