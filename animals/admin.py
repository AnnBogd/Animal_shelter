"""Конфигурации админ-зоны приложения animals."""

from django.contrib import admin
from django.utils.html import format_html

from .models import AdoptionRequest, Animal


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    """Конфигурация отображения животных в административной панели."""

    list_display = ('name', 'species', 'status', 'arrival_date', 'admin_photo')
    list_filter = ('status', 'species')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ['name']}
    fieldsets = [
        ('Основная информация', {
            'fields': (
                'name', 'species', 'breed', 'gender', 'status', 'slug'
            )
        }),
        ('Биография', {'fields': ('bio',)}),
        ('Фото и даты', {
            'fields': (
                'birth_date', 'arrival_date', 'adoption_date', 'photo'
            )
        })
    ]

    @admin.display(description='Фото животного')
    def admin_photo(self, obj: Animal) -> str:
        """Вывести фото животного в админку (при наличии)."""
        if obj.photo:
            return format_html(
                ('<img src="{}" '
                 'style="max-height: 50px; max-width: 50px; '
                 'border-radius: 4px;" />'),
                obj.photo.url
            )
        return "—"


@admin.register(AdoptionRequest)
class AdoptionRequestAdmin(admin.ModelAdmin):
    """Конфигурация отображения заявок в административной панели."""

    list_display = ('animal', 'name', 'phone', 'created_at', 'is_processed')
    list_editable = ('is_processed',)
    list_filter = ('is_processed',)
