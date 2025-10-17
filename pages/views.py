from django.shortcuts import render, get_object_or_404
from .models import SimplePage


def page_detail(request, slug):
    page = get_object_or_404(SimplePage, slug=slug, is_published=True)
    return render(request, 'pages/detail.html', {
        'title': page.title, 
        'page': page,
        'seo_object': page,  # Передаем страницу как SEO-объект
    })
from django.shortcuts import render

# Create your views here.
