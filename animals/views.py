"""View-функции приложения animals."""

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from .models import AdoptionRequest, Animal


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


class BaseAnimalListView(ListView):
    """Базовый CVB для отображения списка животных."""

    model = Animal
    paginate_by = 6
    context_object_name = 'animals'

    def get_queryset(self) -> QuerySet[Animal]:
        """Дополнить queryset фильрацией по имени или виду животного."""
        queryset = super().get_queryset()
        species = self.request.GET.get('species')
        if species:
            queryset = queryset.filter(species=species)
        name = self.request.GET.get('q')
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class ShelterAnimalListView(BaseAnimalListView):
    """CVB для отображения животных, находящихся в приюте."""

    template_name = 'animals/animal_list.html'

    def get_queryset(self) -> QuerySet[Animal]:
        """Дополнить queryset фильрацией - находится в приюте."""
        return super().get_queryset().filter(status='shelter')

    def get_context_data(self, **kwargs) -> dict:
        """Дополнить словарь контекста."""
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q')
        context['species_choices'] = Animal.ANIMAL_CHOICES
        return context


class AdoptedAnimalListView(BaseAnimalListView):
    """CVB для отображения животных, которых забрали домой."""

    template_name = 'animals/adopted_list.html'

    def get_queryset(self) -> QuerySet[Animal]:
        """Дополнить queryset фильрацией - забрали домой, с сортировкой."""
        queryset = super().get_queryset()
        return queryset.filter(status='adopted').order_by('-adoption_date')


class AnimalDetailView(DetailView):
    """CVB для отображения отдельной страницы животного."""

    model = Animal
    template_name = 'animal_detail.html'


class AdoptRequestCreateView(CreateView):
    """CVB для отображения заявок."""

    model = AdoptionRequest
    fields = ('name', 'phone', 'email', 'comment')
    success_url = reverse_lazy('animals:thanks')
    template_name = 'adopt_request_form.html'

    def form_valid(self, form):
        """Привязать животное к форме."""
        animal = get_object_or_404(Animal, pk=self.kwargs['pk'])
        form.instance.animal = animal
        return super().form_valid(form)
