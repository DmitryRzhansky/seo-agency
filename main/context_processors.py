from .models import ServiceCategory

def services_menu(request):
    """
    Добавляет все разделы услуг и связанные с ними услуги в контекст каждого шаблона.
    Используется для построения динамического меню в Header и Footer.
    """
    # Выбираем все категории и предварительно загружаем (select_related/prefetch_related)
    # связанные услуги, чтобы избежать N+1 проблемы с запросами к базе данных.
    categories_with_services = ServiceCategory.objects.prefetch_related('services').order_by('order')

    return {
        'service_categories_menu': categories_with_services
    }