# main/admin.py - Используем улучшенные админ-классы из admin_seo.py

# Импортируем улучшенные админ-классы
from .admin_seo import (
    CityAdmin, ServiceCategoryAdmin, ServiceAdmin, 
    TeamMemberAdmin, TestimonialAdmin, ContactRequestAdmin,
    PortfolioItemAdmin, CustomHeadScriptAdmin, RegionalPostAdaptationAdmin
)

# Импортируем кастомный админ-сайт
from django.contrib import admin

# Регистрируем все модели в кастомном админ-сайте
from .models import City, ServiceCategory, Service, TeamMember, Testimonial, ContactRequest, PortfolioItem, CustomHeadScript, RegionalPostAdaptation

#admin.site.register(City, CityAdmin)
#admin.site.register(ServiceCategory, ServiceCategoryAdmin)
#admin.site.register(Service, ServiceAdmin)
#admin.site.register(TeamMember, TeamMemberAdmin)
#admin.site.register(Testimonial, TestimonialAdmin)
#admin.site.register(ContactRequest, ContactRequestAdmin)
#admin.site.register(PortfolioItem, PortfolioItemAdmin)
#admin.site.register(CustomHeadScript, CustomHeadScriptAdmin)
#admin.site.register(RegionalPostAdaptation, RegionalPostAdaptationAdmin)
