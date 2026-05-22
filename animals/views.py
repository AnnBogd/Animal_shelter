from django.views.generic import TemplateView

from .models import Animal


class HomeView(TemplateView):
    """CBV для отображения главной страницы."""

    template_name = 'animals/home.html'

    def get_context_data(self, **kwargs) -> dict:
        """Дополнить словарь контекста."""
        context = super().get_context_data(**kwargs)
        context['shelter_count'] = (
            Animal
            .objects
            .filter(status='shelter')
            .count()
        )
        context['adopted_count'] = (
            Animal
            .objects
            .filter(status='adopted')
            .count()
        )
        context['recent_animals'] = (
            Animal
            .objects
            .order_by('-arrival_date')[:3])
        return context
