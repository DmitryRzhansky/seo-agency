# main/templatetags/global_filters.py - Глобальные фильтры для совместимости

from django import template
from django.template import Library

# Создаем глобальный регистр для фильтров
register = Library()

@register.filter
def length_is(value, arg):
    """
    Проверяет, равна ли длина значения заданному числу.
    Использование: {{ value|length_is:"1" }}
    Это фильтр для совместимости с Django Unfold.
    """
    try:
        return len(value) == int(arg)
    except (ValueError, TypeError):
        return False

@register.filter
def city_prepositional(city_name):
    """
    Возвращает название города в предложном падеже (в Москве, в Санкт-Петербурге, в Казани).
    Использование: {{ city.name|city_prepositional }}
    """
    if not city_name:
        return city_name
    
    city_name = city_name.strip()
    
    # Специальные случаи
    special_cases = {
        'Москва': 'Москве',
        'Санкт-Петербург': 'Санкт-Петербурге',
        'Нижний Новгород': 'Нижнем Новгороде',
        'Ростов-на-Дону': 'Ростове-на-Дону',
        'Великий Новгород': 'Великом Новгороде',
        'Петропавловск-Камчатский': 'Петропавловске-Камчатском',
        'Южно-Сахалинск': 'Южно-Сахалинске',
        'Комсомольск-на-Амуре': 'Комсомольске-на-Амуре',
        'Сергиев Посад': 'Сергиевом Посаде',
        'Серпухов': 'Серпухове',
        'Химки': 'Химках',
        'Мытищи': 'Мытищах',
        'Королёв': 'Королёве',
        'Люберцы': 'Люберцах',
        'Электросталь': 'Электростали',
        'Железнодорожный': 'Железнодорожном',
        'Балашиха': 'Балашихе',
        'Подольск': 'Подольске',
        'Хабаровск': 'Хабаровске',
        'Владивосток': 'Владивостоке',
        'Якутск': 'Якутске',
        'Магадан': 'Магадане',
        'Благовещенск': 'Благовещенске',
        'Уссурийск': 'Уссурийске',
        'Находка': 'Находке',
        'Артём': 'Артёме',
        'Дальнереченск': 'Дальнереченске',
    }
    
    if city_name in special_cases:
        return special_cases[city_name]
    
    # Общие правила для городов, заканчивающихся на определенные суффиксы
    if city_name.endswith('ск'):
        return city_name[:-2] + 'ске'
    elif city_name.endswith('цк'):
        return city_name[:-2] + 'цке'
    elif city_name.endswith('нск'):
        return city_name[:-3] + 'нске'
    elif city_name.endswith('тск'):
        return city_name[:-3] + 'тске'
    elif city_name.endswith('рск'):
        return city_name[:-3] + 'рске'
    elif city_name.endswith('льск'):
        return city_name[:-4] + 'льске'
    elif city_name.endswith('ов'):
        return city_name[:-2] + 'ове'
    elif city_name.endswith('ев'):
        return city_name[:-2] + 'еве'
    elif city_name.endswith('ин'):
        return city_name[:-2] + 'ине'
    elif city_name.endswith('ын'):
        return city_name[:-2] + 'ыне'
    elif city_name.endswith('ан'):
        return city_name[:-2] + 'ане'
    elif city_name.endswith('ен'):
        return city_name[:-2] + 'ене'
    elif city_name.endswith('ун'):
        return city_name[:-2] + 'уне'
    elif city_name.endswith('а'):
        return city_name[:-1] + 'е'
    elif city_name.endswith('я'):
        return city_name[:-1] + 'е'
    elif city_name.endswith('ь'):
        return city_name[:-1] + 'е'
    else:
        # Если не подходит ни одно правило, добавляем "е"
        return city_name + 'е'

@register.filter
def format_population(population):
    """
    Форматирует численность населения с точками как разделителями тысяч.
    Предполагается, что в базе данных число хранится в тысячах.
    Использование: {{ city.population|format_population }}
    """
    if not population:
        return "0"
    
    try:
        # Число в базе данных хранится в тысячах, поэтому умножаем на 1000
        pop = int(float(population) * 1000)
        
        # Форматируем число с точками как разделителями тысяч
        formatted = f"{pop:,}".replace(",", ".")
        
        return formatted
            
    except (ValueError, TypeError):
        return str(population)
