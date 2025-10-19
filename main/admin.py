# main/admin.py - Используем улучшенные админ-классы из admin_seo.py

# Импортируем улучшенные админ-классы
from .admin_seo import (
    CityAdmin, ServiceCategoryAdmin, ServiceAdmin, 
    TeamMemberAdmin, TestimonialAdmin, ContactRequestAdmin,
    PortfolioItemAdmin, CustomHeadScriptAdmin, RegionalPostAdaptationAdmin
)

# Импортируем кастомный админ-сайт
from .admin_site import admin_site

# Регистрируем все модели в кастомном админ-сайте
from .models import City, ServiceCategory, Service, TeamMember, Testimonial, ContactRequest, PortfolioItem, CustomHeadScript, RegionalPostAdaptation

admin_site.register(City, CityAdmin)
admin_site.register(ServiceCategory, ServiceCategoryAdmin)
admin_site.register(Service, ServiceAdmin)
admin_site.register(TeamMember, TeamMemberAdmin)
admin_site.register(Testimonial, TestimonialAdmin)
admin_site.register(ContactRequest, ContactRequestAdmin)
admin_site.register(PortfolioItem, PortfolioItemAdmin)
admin_site.register(CustomHeadScript, CustomHeadScriptAdmin)
admin_site.register(RegionalPostAdaptation, RegionalPostAdaptationAdmin)