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
        'Москва': 'в Москве',
        'Санкт-Петербург': 'в Санкт-Петербурге',
        'Нижний Новгород': 'в Нижнем Новгороде',
        'Ростов-на-Дону': 'в Ростове-на-Дону',
        'Великий Новгород': 'в Великом Новгороде',
        'Петропавловск-Камчатский': 'в Петропавловске-Камчатском',
        'Южно-Сахалинск': 'в Южно-Сахалинске',
        'Комсомольск-на-Амуре': 'в Комсомольске-на-Амуре',
        'Сергиев Посад': 'в Сергиевом Посаде',
        'Казань': 'в Казани',
        'Новосибирск': 'в Новосибирске',
        'Екатеринбург': 'в Екатеринбурге',
        'Самара': 'в Самаре',
        'Омск': 'в Омске',
        'Уфа': 'в Уфе',
        'Красноярск': 'в Красноярске',
        'Воронеж': 'в Воронеже',
        'Пермь': 'в Перми',
        'Волгоград': 'в Волгограде',
        'Минск': 'в Минске',
        'Алматы': 'в Алмате',
        'Астана': 'в Астане',
        'Ташкент': 'в Ташкенте',
        'Серпухов': 'в Серпухове',
        'Химки': 'в Химках',
        'Мытищи': 'в Мытищах',
        'Королёв': 'в Королёве',
        'Люберцы': 'в Люберцах',
        'Электросталь': 'в Электростали',
        'Железнодорожный': 'в Железнодорожном',
        'Балашиха': 'в Балашихе',
        'Подольск': 'в Подольске',
        'Хабаровск': 'в Хабаровске',
        'Владивосток': 'в Владивостоке',
        'Якутск': 'в Якутске',
        'Магадан': 'в Магадане',
        'Благовещенск': 'в Благовещенске',
        'Уссурийск': 'в Уссурийске',
        'Находка': 'в Находке',
        'Артём': 'в Артёме',
        'Дальнереченск': 'в Дальнереченске',
    }
    
    if city_name in special_cases:
        return special_cases[city_name]
    
    # Общие правила для городов, заканчивающихся на определенные суффиксы
    if city_name.endswith('ск'):
        return f"в {city_name[:-2]}ске"
    elif city_name.endswith('цк'):
        return f"в {city_name[:-2]}цке"
    elif city_name.endswith('нск'):
        return f"в {city_name[:-3]}нске"
    elif city_name.endswith('тск'):
        return f"в {city_name[:-3]}тске"
    elif city_name.endswith('рск'):
        return f"в {city_name[:-3]}рске"
    elif city_name.endswith('льск'):
        return f"в {city_name[:-4]}льске"
    elif city_name.endswith('ов'):
        return f"в {city_name[:-2]}ове"
    elif city_name.endswith('ев'):
        return f"в {city_name[:-2]}еве"
    elif city_name.endswith('ин'):
        return f"в {city_name[:-2]}ине"
    elif city_name.endswith('ын'):
        return f"в {city_name[:-2]}ыне"
    elif city_name.endswith('ан'):
        return f"в {city_name[:-2]}ане"
    elif city_name.endswith('ен'):
        return f"в {city_name[:-2]}ене"
    elif city_name.endswith('ун'):
        return f"в {city_name[:-2]}уне"
    elif city_name.endswith('а'):
        return f"в {city_name[:-1]}е"
    elif city_name.endswith('я'):
        return f"в {city_name[:-1]}е"
    elif city_name.endswith('ь'):
        return f"в {city_name[:-1]}е"
    else:
        # Если не подходит ни одно правило, добавляем "е"
        return f"в {city_name}е"

