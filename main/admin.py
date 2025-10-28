# main/admin.py - Используем улучшенные админ-классы из admin_seo.py

# Импортируем улучшенные админ-классы
from .admin_seo import (
    CityAdmin, ServiceCategoryAdmin, ServiceAdmin, 
    TeamMemberAdmin, TestimonialAdmin, ContactRequestAdmin,
    PortfolioItemAdmin, PortfolioCategoryAdmin, CustomHeadScriptAdmin, RegionalPostAdaptationAdmin,
    FAQCategoryAdmin, FAQItemAdmin, GlossaryCategoryAdmin, GlossaryTermAdmin
)

# Импортируем кастомный админ-сайт
from django.contrib import admin

# Регистрируем все модели в кастомном админ-сайте
from .models import City, ServiceCategory, Service, TeamMember, Testimonial, ContactRequest, PortfolioItem, PortfolioCategory, CustomHeadScript, RegionalPostAdaptation, FAQCategory, FAQItem, GlossaryCategory, GlossaryTerm, Author

# Все модели уже зарегистрированы через декораторы @admin.register() в admin_seo.py
# Регистрируем только City, так как у неё нет декоратора
admin.site.register(City, CityAdmin)
